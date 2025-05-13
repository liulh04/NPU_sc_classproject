package com.example.taskhelpapp;

import android.content.pm.PackageManager;
import android.location.Location;
import android.os.Bundle;
import android.widget.Button;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;

import com.baidu.mapapi.map.BaiduMap;
import com.baidu.mapapi.map.MapView;
import com.baidu.mapapi.map.MyLocationConfiguration;
import com.baidu.mapapi.map.MyLocationData;
import com.baidu.mapapi.model.LatLng;
import com.baidu.mapapi.map.MapStatus;
import com.baidu.mapapi.map.MapStatusUpdateFactory;
import com.baidu.mapapi.CoordType;
import com.baidu.mapapi.SDKInitializer;
import com.baidu.location.BDLocation;
import com.baidu.location.BDLocationListener;
import com.baidu.location.LocationClient;
import com.baidu.location.LocationClientOption;

public class MainActivity extends AppCompatActivity {

    static {
        System.loadLibrary("BaiduMapSDK_base_v7_6_4");
        System.loadLibrary("BaiduMapSDK_map_v7_6_4"); // 如果需要，也加载地图相关的库
    }

    private Button publishTaskButton;
    private Button helpTaskButton;
    private Button profileButton;
    private Button locateButton;  // 定位按钮
    private MapView mapView;
    private BaiduMap baiduMap;

    // 定位相关
    private LocationClient mLocationClient;
    private BDLocationListener mBDLocationListener;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // 百度地图 SDK 初始化
        SDKInitializer.initialize(getApplicationContext());
        SDKInitializer.setCoordType(CoordType.BD09LL);  // 设置坐标类型为 BD09

        // 获取控件
        publishTaskButton = findViewById(R.id.publish_task_button);
        helpTaskButton = findViewById(R.id.help_task_button);
        profileButton = findViewById(R.id.profile_button);
        locateButton = findViewById(R.id.locate_button);  // 定位按钮

        // 初始化地图
        mapView = findViewById(R.id.map_view);
        baiduMap = mapView.getMap();
        baiduMap.setMyLocationEnabled(true);

        // 设置定位模式
        baiduMap.setMyLocationConfiguration(new MyLocationConfiguration(
                MyLocationConfiguration.LocationMode.NORMAL, true, null));

        // 初始化定位客户端
        try {
            mLocationClient = new LocationClient(getApplicationContext());
        } catch (Exception e) {
            throw new RuntimeException(e);
        }

        mBDLocationListener = new BDLocationListener() {
            @Override
            public void onReceiveLocation(BDLocation bdLocation) {
                if (bdLocation != null && bdLocation.getLocType() == BDLocation.TypeGpsLocation) {
                    MyLocationData locData = new MyLocationData.Builder()
                            .latitude(bdLocation.getLatitude())
                            .longitude(bdLocation.getLongitude())
                            .build();
                    baiduMap.setMyLocationData(locData);

                    // 移动地图到当前位置
                    LatLng latLng = new LatLng(bdLocation.getLatitude(), bdLocation.getLongitude());
                    MapStatus.Builder builder = new MapStatus.Builder();
                    builder.target(latLng).zoom(18.0f);  // 设置缩放级别
                    baiduMap.animateMapStatus(MapStatusUpdateFactory.newMapStatus(builder.build()));
                }
            }
        };

        // 配置定位参数
        LocationClientOption option = new LocationClientOption();
        option.setIsNeedAddress(true);
        option.setCoorType("bd09ll");  // 设置坐标类型
        mLocationClient.setLocOption(option);

        // 设置定位监听器
        mLocationClient.registerLocationListener(mBDLocationListener);

        // 使用 try-catch 处理可能的异常
        try {
            // 开始定位
            mLocationClient.start();
        } catch (Exception e) {
            e.printStackTrace();
            Toast.makeText(this, "定位初始化失败: " + e.getMessage(), Toast.LENGTH_SHORT).show();
        }

        // 请求定位权限
        if (ActivityCompat.checkSelfPermission(this, android.Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED
                && ActivityCompat.checkSelfPermission(this, android.Manifest.permission.ACCESS_COARSE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
            ActivityCompat.requestPermissions(this, new String[]{android.Manifest.permission.ACCESS_FINE_LOCATION}, 1);
        }

        // 定位按钮点击事件
        locateButton.setOnClickListener(v -> {
            // 获取当前定位并更新地图
            try {
                if (mLocationClient != null && mLocationClient.isStarted()) {
                    mLocationClient.requestLocation();
                } else {
                    Toast.makeText(this, "定位失败", Toast.LENGTH_SHORT).show();
                }
            } catch (Exception e) {
                e.printStackTrace();
                Toast.makeText(this, "请求定位失败: " + e.getMessage(), Toast.LENGTH_SHORT).show();
            }
        });

        // 设置按钮点击事件
        publishTaskButton.setOnClickListener(v -> openPublishTaskPage());
        helpTaskButton.setOnClickListener(v -> openHelpTaskPage());
        profileButton.setOnClickListener(v -> openProfilePage());
    }

    // 请求权限结果回调
    @Override
    public void onRequestPermissionsResult(int requestCode, String[] permissions, int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        if (requestCode == 1) {
            if (grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                Toast.makeText(this, "权限已获得", Toast.LENGTH_SHORT).show();
            } else {
                Toast.makeText(this, "权限未授予，无法获取位置", Toast.LENGTH_SHORT).show();
            }
        }
    }

    private void openPublishTaskPage() {
        // 打开发布任务页面
    }

    private void openHelpTaskPage() {
        // 打开帮助任务页面
    }

    private void openProfilePage() {
        // 打开个人资料页面
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        if (mLocationClient != null) {
            mLocationClient.stop();  // 停止定位
        }
        mapView.onDestroy();
    }

    @Override
    protected void onResume() {
        super.onResume();
        mapView.onResume();
    }

    @Override
    protected void onPause() {
        super.onPause();
        mapView.onPause();
    }
}
