# プログラムでロボットを動かす方法
今週の実習ではロボットアームとグリッパの開閉をプログラムで実現する方法を学びます。このデモプログラムを応用すると産業用ロボットで最もよく使われるピック＆プレースを実現できます。

なお、このプログラムは東京オープンソースロボティクス協会の次のウェブサイトを参考にしました．

https://opensource-robotics.tokyo.jp/?p=4526

ロボットグリッパの制御は以下のgithubを参考にしました.

https://github.com/DougUOW/om_moveit_examples/blob/master/src/testing_effort.py

## 実行方法
１番目のUbuntu端末を開き、次のコマンドでRviz（ROSの視覚化ツール）やGazeboを起動する。
```
$ source ~/.bashrc
$ sudo chmod 777 /dev/ttyUSB0
$ roslaunch open_manipulator_controllers joint_trajectory_controller.launch sim:=false
```
２番目の端末を開き、次のコマンドでロボットアームを動かす。
```
$ cd ~/catkin_ws/src/open_manipulator/open_manipulator_controller/scripts
$ python3 arm_demo2.py
```