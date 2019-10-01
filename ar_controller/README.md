## ar_controller

## 概要
Intel Realsense R200により取得した画像からARタグを認識し、シミュレーター上のロボットを動かします。サンプルコードでは、所定のARタグを認識するとロボットが前進するようになっていますが、ARタグの位置・姿勢によってロボットを制御することも可能ですのでアレンジしてみてください。

### 動作環境
* Ubuntu 16.04
* ROS Kinetic Kame Desktop-full
** [ar_track_alvar](http://wiki.ros.org/ar_track_alvar)
** [realsense_camera](http://wiki.ros.org/realsense_camera)

### 前準備
実世界とカメラモデルを対応づけるカメラキャリブレーションという作業が必要です。[こちらのページ](http://robot.isc.chubu.ac.jp/?p=1063)にカメラキャリブレーションの方法を記載してますので参考にしてください。  

リンク先のページではUSBカメラを使用していますが、ここではIntelのrealsense R200を使用します。
realsense R200をROSで使用するために、下記のlaunchを起動します。

```
$ roslaunch realsense_camera r200_nodelet_rgbd.launch
```

上記のコマンドでカメラが使用できる状態になりますので、画像に関するトピックが配信されます。次にカメラキャリブレーションを行います。USBカメラを使用する場合と異なり、画像のトピック名が変わるので注意してください。

```
$ rosrun camera_calibration cameracalibrator.py --size 8x6 --square 0.0245 image:=/camera/rgb/image_color
```

カメラキャリブレーションが完了したら、キャリブレーションデータをar_controllerパッケージに移動しましょう。下記のWORKSPACEはROSのワークスペースです。作成したワークスペース名に置き換えてください。

```
$ cd ~/WORKSPACE/src/ar_controller/
$ mkdir calibrationdata
$ mv /tmp/calibrationdata.tar.gz ./calibrationdata/
$ cd calibrationdata
$ tar xzvf calibrationdata.tar.gz
```

最後にar_track_alvarを用いてARタグを認識するために準備します。launchディレクトリにar_track.launchを用意してますので、こちらを修正して使用してください。こちらのlaunchファイルでは、Realsenseを使用するためのlaunchファイル、ar_track_alvarによるARタグ認識、可視化ツールであるrvizを起動するようになっています。

先ほどカメラキャリブレーションにて作成したost.yamlファイルを読み込めるようにします。下記の例に示すar_track.launchの5行目にてost.yamlを読み込んでます。ost.yamlが存在するパスを正しく記述する必要があるので修正してください。フルパスで記述する必要があるので注意してください。

```
<param name="camera_info_url" type="string" value="file:///home/yuu/catkin_ws/src/ar_controller/calibrationdata/ost.yaml" />
```

### 実行
先ほど修正したlaunchファイルを起動します。
catkin_make、環境変数の設定をした後にlaunchファイルを実行しましょう。
```
$ cd ~/WORKSPACE
$ catkin_make
$ source devel/setup.bash
$ roslaunch ar_controller ar_track.launch
```

最後にサンプルコードを実行します。
まずは新しいウィンドウを開き、シミュレータを起動しましょう。
```
rosrun turtlesim turtlesim_node
```

新しいウィンドウを開き、下記のようにのノードを実行してください。
```
rosrun ar_controller ar_controller.py
```
上記のコマンドを実行しただけではロボットは動きませんが、こちらのページにある真ん中のARタグ(ID4番)を認識するとロボットが動きます。

サンプルプログラムではARタグの位置と姿勢をターミナルに出力しています。こちらの情報を使ってロボットを操縦できるようにサンプルプログラムを改良してみましょう。
