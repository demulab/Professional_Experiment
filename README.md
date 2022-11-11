# 専門実験 OpenManipulator-X & AR-Detection

## 概要
OpenManipulator-XによるARマーカのピック&プレース。

## 使用製品
- OpenManipulator-X
- WebCamera(Logicool)

## 開発環境
- Ubuntu 20.04
- ROS Noetic

## 使用するパッケージ
- OpenManipulator-X関連
    - 詳しくは[demura.net](https://demura.net/education/lecture/21651.html)や[ROBOTIS公式](https://emanual.robotis.com/docs/en/platform/openmanipulator_x/overview/)を参照
- ar_track_alvar (非公式Noetic-devel)
    - Noeticだと公式でbranchやaptでリリースしていない (2021年12月時点)
    - 現時点で非公式で有志がNoetic用に変更した[パッケージ](https://github.com/machinekoder/ar_track_alvar/tree/noetic-devel)を利用
- usb_cam

## 実行方法
### ARマーカのピック&プレース
- 1つ目のターミナル

Moveitを起動する。

```
sudo chmod 777 /dev/ttyUSB0

roslaunch open_manipulator_controllers joint_trajectory_controller.launch sim:=false
```

- 2つ目のターミナル

カメラとARマーカ認識プログラムを起動する。

```
sudo chmod +x /dev/videoxxx
(xxx: ウェブカメラのデバイス番号)

roslaunch experiment camera_bringup.launch video_device:=/dev/videoxxx
```

- 3つ目のターミナル

ARマーカをピック＆プレースする。

```
roscd experiment/script
python3 ar_picking_demo.py
```

## 付録
### ①OpenManipulator-X座標軸

ROSの座標軸では赤,緑,青の順にx,y,zに対応している。

![image](https://user-images.githubusercontent.com/42795206/199896505-963f452c-91a2-406c-b6f3-8a31c1e9ec68.png)


以下の画像は、OpenManipulator-Xのエンドエフェクタ座標軸。

![image](https://user-images.githubusercontent.com/42795206/199895712-15ec1155-540e-475b-aee2-1ae4142e698c.png)

### ②ウェブカメラのキャリブレーション
#### 目的
ar_track_alvarを使用する場合，カメラのイメージトピック(/camera_raw), 内部パラメータトピック(/camera_info)が必要となる

webカメラ(Logicool)をROSで扱う場合，内部パラメータトピック(/camera_info)の値が欠損している

つまり，**内部パラメータを自分たちでキャリブレーションを通して情報付与する必要がある**

#### 手順
##### 1. キャリブレーションパッケージのインストール
```
sudo apt install -y ros-noetic-camera-calibration

sudo apt install -y ros-noetic-image-proc
```

##### 2. チェッカーボードの印刷
- [チェッカーボード](http://wiki.ros.org/camera_calibration/Tutorials/MonocularCalibration?action=AttachFile&do=get&target=check-108.pdf)を保存してA4で印刷する
- チェックの交点が8x6個，一辺が0.025mの格子が描画された紙だったらOK

(OpenManipulator No.10機体には既に，私が印刷したチェッカーボードを置いてある)

##### 3. 測定
- 1つ目のターミナル
```
roscore
```

- 2つ目のターミナル
```
sudo chmod +x /dev/videoxxx
(xxx: ウェブカメラのデバイス番号)

rosrun usb_cam usb_cam_node _video_devide:=/dev/videoxxx
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

##### 4. 測定結果と取り出し
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

camera.yamlを/experiment/config/に保存する。


### ③ARマーカの印刷
3.0cmのマーカを生成する。
```
rosrun ar_track_alvar createMarker -s 3.0 -p
```

### ④プロキシ設定
.bashrc
```
export http_proxy="http://wwwproxy.kanazawa-it.ac.jp:8080"
export https_proxy="http://wwwproxy.kanazawa-it.ac.jp:8080"
```
/etc/apt/apt.conf
```
Acquire::http::Proxy "http://wwwproxy.kanazawa-it.ac.jp:8080";
Acquire::https::Proxy "http://wwwproxy.kanazawa-it.ac.jp:8080";
```
