# Task

LinuxのPREEMPT_RTは、TwinCATに求められる様々な要件が満たされたカーネル機能を提供しています。

## CPUの隔離機能

TwinCATからIsolateコアを設定すると、リアルタイムプロセスが一般プロセスに割り当てられないようにするカーネルパラメータが渡されます。起動後次のコマンドでパラメータの設定状態を確認することができます。

```{code} bash
cat /proc/cmdline | grep isolcpus
```

shared/isolated = 2/2の場合
    : ```{code} bash
      root=gpt-auto ro quiet splash rootwait intel_iommu=on iommu=pt efi=runtime rd.luks=0 irqaffinity=0-1 isolcpus=2-N rcu_nocbs=2-N
      ```

shared/isolated = 4/0の場合
    : ```{code} bash
      root=gpt-auto ro quiet splash rootwait intel_iommu=on iommu=pt efi=runtime rd.luks=0 irqaffinity=0-3 isolcpus=4-N rcu_nocbs=4-N
      ```

```{tip}
参考
    : [https://realtime-linux.org/getting-started-with-preempt_rt-guide/](https://realtime-linux.org/getting-started-with-preempt_rt-guide/)
```