# MoveIt! チュートリアル
MoveIt！はROSでロボットアームの運動学、逆運動学、モーションプランニング（軌道計画）を担当する重要なパッケージ（ある機能を持ったソフトウェアの集合）です。ここではMoveIt!を使ってロボットを動かします。
## 実機の動かし方
ロボットの電源を入れ，ノートパソコンとロボットをUSBケーブルで接続する端末を開き、次のコマンドを実行するとRvizが起動する．
```
$ source ~/.bashrc
$ sudo chmod 777 /dev/ttyUSB0
$ roslaunch open_manipulator_controllers joint_trajectory_controller.launch sim:=false
```
シミュレータと同様にRvizのインターラクティブマーカやPlanningのボタンを押して軌道を生成されて実行する．実機もRvizと同じ軌道を移動する。動いたら成功！