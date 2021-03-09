# bwt901cl_pkg

IMUセンサのひとつであるBWT901CLをROS2で使うためのpackageです．

### 構成

- package: bwt901cl_pkg
    - node: imu_bwt901cl(publisher type)
    - msg:
        - Imu: '/sensor/bwt901cl/imu'
        - MagneticField: '/sensor/bwt901cl/MagneticField'
        - Temperature: '/sensor/bwt901cl/Temperature'
        - Vector3: '/sensor/bwt901cl/Angle'

### build

```
colcon build --packages-select bwt901cl_pkg
```

### run

```
ros2 run bwt901cl_pkg imu_bwt901cl
```

### 注意点

- BWT901CLをchmodで実行できるようにしていないと，`permission dennied`が出る．

# 参考ページ

https://github.com/WITMOTION/BWT901CL

https://github.com/ros2/common_interfaces

https://sgrsn1711.hatenablog.com/entry/2018/02/14/204044