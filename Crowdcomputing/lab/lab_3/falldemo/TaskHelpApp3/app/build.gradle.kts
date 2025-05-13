plugins {
    id("com.android.application") // 插件的 ID 必须用双引号括起来
}

android {
    namespace = "com.example.taskhelpapp"
    compileSdk = 35

    defaultConfig {
        applicationId = "com.example.taskhelpapp"
        minSdk = 21
        targetSdk = 35
        versionCode = 1
        versionName = "1.0"

        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
    }

    buildTypes {
        release {
            isMinifyEnabled = false
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
        }
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_11
        targetCompatibility = JavaVersion.VERSION_11
    }

    // 配置 jniLibs 目录，确保只使用 x86_64 架构的 .so 文件
    sourceSets {
        getByName("main") {
            // 使用 setSrcDirs 来设置目录
            jniLibs.setSrcDirs(listOf("libs/x86_64"))  // 仅使用 x86_64 架构的 .so 文件
        }
    }
}

dependencies {
    // 引入百度 SDK JAR 文件
    implementation(files("libs/BaiduLBS_Android.jar"))

    implementation("androidx.appcompat:appcompat:1.3.1")
    implementation("com.google.android.material:material:1.6.0") // 更新为支持 Material3 的版本
    implementation("androidx.constraintlayout:constraintlayout:2.1.0")
    implementation("androidx.recyclerview:recyclerview:1.2.1")
    testImplementation("junit:junit:4.13.2")
    androidTestImplementation("androidx.test.ext:junit:1.1.3")
    androidTestImplementation("androidx.test.espresso:espresso-core:3.4.0")
}
