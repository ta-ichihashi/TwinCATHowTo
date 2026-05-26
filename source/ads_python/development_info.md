# Notificationを用いたデータ収集ライブラリのコード解説

```{admonition} Githubサンプルコード
:class: info

250 $\mu s$ のサイクルタイムのPLCタスクの変数データをNotificationで収集するサンプルコードです。詳細はGithubのREADME.MDをご覧ください。

[https://github.com/Beckhoff-JP/Python_ADS_Sample](https://github.com/Beckhoff-JP/Python_ADS_Sample)
```

まず、pyadsが扱える構造体のデータ定義を`model.py` に定義します。タプル型でTwinCATの構造体データのモデルを定義します。{ref}`code_axis_toplc` はNC PTPのモータ軸のPLCへの公開変数を定義した構造体 `NCTOPLC_AXIS_REF` を定義したものです。

```{code-block} python
:name: code_axis_toplc
:caption: model.py への定義
# NC PTP axis to_plc

axis_to_plc_structure=(
    ("StateDWord", pyads.PLCTYPE_DWORD,1),
    ("ErrCode", pyads.PLCTYPE_UDINT,1),
    ("AxisState", pyads.PLCTYPE_UDINT,1),
    ("AxisModeConfirmation", pyads.PLCTYPE_UDINT,1),
    ("HomingState", pyads.PLCTYPE_UDINT,1),
    ("CoupleState", pyads.PLCTYPE_UDINT,1),
    ("SvbEntries", pyads.PLCTYPE_UDINT,1),
    ("SafEntries", pyads.PLCTYPE_UDINT,1),
    ("AxisId", pyads.PLCTYPE_UDINT,1),
    ("OpModeDWord", pyads.PLCTYPE_DWORD,1),
    ("ActPos", pyads.PLCTYPE_LREAL,1),
    ("ActPosModulo", pyads.PLCTYPE_LREAL,1),
    ("ActiveControlLoopIndex", pyads.PLCTYPE_UINT,1),
    ("ControlLoopIndex", pyads.PLCTYPE_UINT,1),
    ("ModloActTurns", pyads.PLCTYPE_DINT,1),
    ("ActVelo", pyads.PLCTYPE_LREAL,1),
    ("PosDiff", pyads.PLCTYPE_LREAL,1),
    ("SetPos", pyads.PLCTYPE_LREAL,1),
    ("SetVelo", pyads.PLCTYPE_LREAL,1),
    ("SetAcc", pyads.PLCTYPE_LREAL,1),
    ("TargetPos", pyads.PLCTYPE_LREAL,1),
    ("ModuloSetPos", pyads.PLCTYPE_LREAL,1),
    ("ModloSetTurns", pyads.PLCTYPE_DINT,1),
    ("CmdNo", pyads.PLCTYPE_UINT,1),
    ("CmdState", pyads.PLCTYPE_UINT,1),
    ("SetJerk", pyads.PLCTYPE_LREAL,1),
    ("SetTorque", pyads.PLCTYPE_LREAL,1),
    ("ActTorque", pyads.PLCTYPE_LREAL,1),
    ("StateDWord2", pyads.PLCTYPE_DWORD,1),
    ("StateDWord3", pyads.PLCTYPE_DWORD,1),
    ("TouchProbeState", pyads.PLCTYPE_DWORD,1),
    ("TouchProbeCounter", pyads.PLCTYPE_DWORD,1),
    ("CamCouplingState", pyads.PLCTYPE_SINT,8),
    ("CamCouplingTableID", pyads.PLCTYPE_UINT,8),
    ("ActTorqueDerivative", pyads.PLCTYPE_LREAL,1),
    ("SetTorqueDerivative", pyads.PLCTYPE_LREAL,1),
    ("AbsPhasingPos", pyads.PLCTYPE_LREAL,1),
    ("TorqueOffset", pyads.PLCTYPE_LREAL,1),
    ("ActPosWithoutPosCorrection", pyads.PLCTYPE_LREAL,1),
    ("ActAcc", pyads.PLCTYPE_LREAL,1),
    ("DcTimeStamp", pyads.PLCTYPE_UDINT,1),
    ("_reserved2", pyads.PLCTYPE_USINT,4),
    ("UserData", pyads.PLCTYPE_LREAL,1),
)
```

次に、{ref}`code_pbserver_class` のとおり、オブザーバクラスを定義します。`observer()`タスクが実行され、ADSのnotificationを利用して登録した型情報と該当シンボルの値変化を検出したら蓄積されるdequeオブジェクトからデータを取り出して標準出力にプリントアウトするだけのコードです。

```{code-block} python
:name: code_pbserver_class
:caption: オブザーバクラスの定義

from model import axis_to_plc_structure

@dataclass
class MotionWatcherViewModel(BaseEventTask):
    view_store : deque = field(default_factory=lambda : deque(maxlen=1000))

    def __post_init__(self):
        self.receiver = EventReporter(plc=self.ads_connection,
                                         mapping_structure=axis_to_plc_structure,
                                         mapping_symbol=self.watch_symbol,
                                         packkaged_num=1)

    async def observer(self):
        while len(self.receiver.queue) > 0:
            record = self.receiver.queue.pop()
            self.view_store.appendleft(record)
        print(self.view_store)
        await asyncio.sleep(3)
```

````{tip}


{numref}`code_pbserver_class` のオブザーバクラスは`BaseEventTask`を継承しています。また、インターフェース`IEventTask`インターフェースの実装でもあります。

このインターフェースで定義された `observer_task()` を{ref}`code_task_manager`にて並列処理タスク化しています。

`observer_task()`は、`observer()` を周期実行するタスクです。つまり、ユーザは任意の`obverver()`を定義することで、周期実行しながら Notification により通知された構造体データの OrderdDict の deque 

```{mermaid}
   classDiagram

        class MotionWatcherViewModel {
            +view_store deque = deque(maxlen=1000)
            +observer()
        }


       class BaseEventTask {
           +ads_connection AdsCommunication
           +mapping_model tuple
           +watch_symbol str
           +observer_task()
       }

       class IEventTask {
           +observer()
       }

       IEventTask <|.. BaseEventTask 
       BaseEventTask <|-- MotionWatcherViewModel
```

```{code-block} python
@dataclass
class IEventTask(ABC):
    @abstractmethod
    async def observer(self):
        pass

    @abstractmethod
    async def observer_task(self):
        pass


@dataclass
class BaseEventTask(IEventTask):
    ads_connection : AdsCommunication
    mapping_model : tuple = field(default_factory=tuple)
    watch_symbol : str = field(default_factory=str)

    async def observer_task(self):
        while True:
            await self.observer()
```
````


並行タスクを登録、実行するクラスをメインプログラムに定義します。（{num_ref}`code_task_manager`）

```{code-block} python
:name: code_task_manager
:caption: 並列タスク管理クラス

class TaskManager:
    def __init__(self):
        self.tasks = []

    def add_task(self, task: IEventTask):
        self.tasks.append(task)

    async def run_tasks(self):
        await asyncio.gather(*(task.observer_task() for task in self.tasks))
```


```{code-block} python
:name: code_main_program
:caption: メインプログラム

async def main():

    ams_net_id = os.getenv('CONTAINER_AMSID', default='199.4.42.250.1.1')
    hostname = os.getenv('CONTAINER_HOSTNAME', default='tc31-xar')

    motion_connector = AdsCommunication(ams_net_id=ams_net_id,
                                    ads_port=501,
                                    host_address=hostname)

    plc_connector = AdsCommunication(ams_net_id=ams_net_id,
                                    ads_port=851,
                                    host_address=hostname)


    motion_observer = MotionWatcherViewModel(
        ads_connection=motion_connector,
        watch_symbol='Axes.Axis 1.ToPlc'
        )

    job_observer = JobWatcherViewModel(
        ads_connection=plc_connector,
        watch_symbol='demo3.runner.event_message'
        )

    task_manager = TaskManager()
    task_manager.add_task(motion_observer)
    task_manager.add_task(job_observer)
    await task_manager.run_tasks()

if __name__ == '__main__':
    asyncio.run(main())

```