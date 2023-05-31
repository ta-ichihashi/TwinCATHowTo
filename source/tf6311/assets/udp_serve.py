import asyncio
from struct import pack, unpack
import random

class DummyMeasurementMachineProtocol:

    def __init__(self):
        self.counter = 0;

    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        """
        受信イベントハンドラ
         struct.pack/unpackは以下のドキュメント参照のこと。
         https://docs.python.org/ja/3/library/struct.html
         PLCからデータ受信したバイトデータ data を以下の変数へ展開。
         '<'   : リトルエンディアンのバイト配列として解釈
         '5s'  : 5Byte 文字列を、 commandへ展開し、decode()処理して文字列型へ
         'H'   : unsigned short型（PLCではUINT型）としてsender_sequenceに展開
         'Q'   : unsigned long long int 型 (PLCではULINT型)としてvalueに展開
        """
        command, sender_sequence, value = unpack('<5sHQ', data)
        command = command.decode()
        # 標準出力への表示
        print(f"Received {command}, {sender_sequence}, {value} from {addr}")
        print(f"Send sequence : {self.counter} to {addr}")
        """
        PLCに送信する電文データをバイトデータへパック
         '<'   : リトルエンディアンのバイト配列に組み立てる
         '5s'  : 5Byte 文字列として、'RCOM'という文字にNULLを付加したバイトデータをセット
         'H'   : unsigned short型（PLCではUINT型）として受信回数のカウンタself.counter値をセット
         'f'   : float 型 (PLCではREAL型)としてsender_sequenceを型変換してセット
        """
        send_data = pack('<5sHf', b'RCOM\x00', self.counter, sender_sequence)
        # 組み立てた電文をPLCに送り返す。
        self.transport.sendto(send_data, addr)
        # シーケンス番号を繰り上げる。unsigned shortの最大値（65535）になったらリセット。
        if self.counter < 65535:
            self.counter += 1;
        else:
            self.counter = 0;


loop = asyncio.get_event_loop()
print("Starting UDP server")
# ポート9998のUDPで全ホストからの接続を待つ。
listen = loop.create_datagram_endpoint(
        DummyMeasurementMachineProtocol,
        local_addr=('0.0.0.0', 9998)
    )
transport, protocol = loop.run_until_complete(listen)

try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

transport.close()
loop.close()