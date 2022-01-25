# 専門実験 OpenManipulator-X & AR-Detection

## 概要
- OpenManipulator-Xの実機立ち上げ
- ウェブカメラによるARマーカー認識
- ウェブカメラのキャリブレーション方法も紹介

## 使用製品
- OpenManipulator-X
- WebCamera(Logicool)

## 開発環境
- Ubuntu 20.04
- ROS Noetic

※ OpenManipulator No.10に環境を整えましたので参照ください

## 使用するパッケージ
- OpenManipulator-X関連
    - 詳しくは[demura.net](https://demura.net/education/lecture/21651.html)や[ROBOTIS公式](https://emanual.robotis.com/docs/en/platform/openmanipulator_x/overview/)を参照
- ar_track_alvar (非公式Noetic-devel)
    - Noeticだと公式でbranchやaptでリリースしていない (2021年12月時点)
    - 現時点で非公式で有志がNoetic用に変更した[パッケージ](https://github.com/machinekoder/ar_track_alvar/tree/noetic-devel)を利用
- usb_cam

## 実行方法
- 1つ目のターミナル
```
sudo chmod 777 /dev/ttyUSB0

roslaunch open_manipulator_controllers joint_trajectory_controller.launch sim:=false
```

- 2つ目のターミナル
```
sudo chmod +x /dev/videoxxx
(xxx: ウェブカメラのデバイス番号)

roslaunch experiment camera_bringup.launch video_device:=/dev/videoxxx
```


---
## ウェブカメラの内部キャリブレーション
### 目的
ar_track_alvarを使用する場合，カメラのイメージトピック(/camera_raw), 内部パラメータトピック(/camera_info)が必要となる

webカメラ(Logicool)をROSで扱う場合，内部パラメータトピック(/camera_info)の値が欠損している

つまり，**内部パラメータを自分たちでキャリブレーションを通して情報付与する必要がある**

### 手順
#### 1. キャリブレーションパッケージのインストール
```
sudo apt install -y ros-noetic-camera-calibration

sudo apt install -y ros-noetic-image-proc
```

#### 2. チェッカーボードの印刷
- [チェッカーボード](http://wiki.ros.org/camera_calibration/Tutorials/MonocularCalibration?action=AttachFile&do=get&target=check-108.pdf)を保存してA4で印刷する
- チェックの交点が8x6個，一辺が0.025mの格子が描画された紙だったらOK
(OpenManipulator No.10機体には既に，私が印刷したチェッカーボードを置いてある)

#### 3. 測定
- 1つ目のターミナル
```
roscore
```

- 2つ目のターミナル
```
sudo chmod +x /dev/videoxxx
(xxx: ウェブカメラのデバイス番号)

rosrun usb_cam usb_cam.launch _video_devide:=/dev/videoxxx
```

- 3つ目のターミナル
```
rosrun camera_calibration camearcalibrator.py --size 8x6 --square 0.025 image:=/yyy
(yyy: ウェブカメラのイメージトピック)
```

3つ目のターミナルを実行したら下の写真のようなウィンドウが開きます
チェッカーボードを色々な見せ方で見せて測定を行ってください

  - 上手くキャリブレーションさせるコツ
    - 様々な距離で撮る
    - 画角隅々まで撮る
    - チェッカーボードを斜め等にして撮る

<div style="text-align: center;">
  <img src="https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.amazonaws.com%2F0%2F254442%2F660795cd-98fb-7113-8baf-5bc5cd7ef491.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&w=1400&fit=max&s=5a3e7e42ee775cb175ebcd2dcaba5530">
</div>

ウィンドウ右にある青い「CALIBRATE」が押せるようになったら測定は十分となり，ボタンを押すとキャリブレーションの計算が始まります
この計算は数分かかります

#### 4. 測定結果と取り出し
`/tmp/calibrationdata.tar.gz`に 3. の測定結果が保存されています
以下の操作で解答及びファイルのリネームをします

```
tar -xvzf /tmp/calibrationdata.tar.gz
mv ost.yaml camera.yaml
```

camera.yamlを開き，以下のように修正します
```yaml=
camera_name: narrow_stereo # この行を
camera_name: camera        # このように修正
```

camera.yamlを任意の位置に設定します
(No.10機体のUbuntuではexperimentパッケージ内に設定しました)
