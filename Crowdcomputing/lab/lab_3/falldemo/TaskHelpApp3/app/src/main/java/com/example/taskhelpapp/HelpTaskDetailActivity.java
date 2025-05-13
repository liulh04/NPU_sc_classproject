package com.example.taskhelpapp;

import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.provider.MediaStore;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import androidx.activity.result.ActivityResultCallback;
import androidx.activity.result.contract.ActivityResultContracts;
import androidx.appcompat.app.AppCompatActivity;

public class HelpTaskDetailActivity extends AppCompatActivity {

    private TextView taskTitleTextView;
    private TextView taskDescriptionTextView;
    private TextView taskLocationTextView;
    private Button uploadFileButton;
    private Button uploadImageButton;

    private static final int PICK_FILE_REQUEST_CODE = 1; // 文件选择请求代码
    private static final int PICK_IMAGE_REQUEST_CODE = 2; // 相机拍照请求代码

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_help_task_detail);

        taskTitleTextView = findViewById(R.id.task_title);
        taskDescriptionTextView = findViewById(R.id.task_description);
        taskLocationTextView = findViewById(R.id.task_location);
        uploadFileButton = findViewById(R.id.upload_file_button);
        uploadImageButton = findViewById(R.id.upload_image_button);

        // 从 Intent 获取传递的任务信息
        String taskTitle = getIntent().getStringExtra("taskTitle");
        String taskDescription = getIntent().getStringExtra("taskDescription");
        String taskLocation = getIntent().getStringExtra("taskLocation");

        taskTitleTextView.setText(taskTitle);
        taskDescriptionTextView.setText(taskDescription);
        taskLocationTextView.setText(taskLocation);

        // 设置上传文件按钮的点击事件
        uploadFileButton.setOnClickListener(v -> openFileChooser());

        // 设置上传图片按钮的点击事件
        uploadImageButton.setOnClickListener(v -> openCamera());
    }

    // 打开文件选择器，用户选择文件
    private void openFileChooser() {
        Intent intent = new Intent(Intent.ACTION_GET_CONTENT);
        intent.setType("*/*"); // 设置文件类型为所有文件
        intent.addCategory(Intent.CATEGORY_OPENABLE);
        startActivityForResult(intent, PICK_FILE_REQUEST_CODE);
    }

    // 打开相机，拍照并返回图片
    private void openCamera() {
        Intent intent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
        if (intent.resolveActivity(getPackageManager()) != null) {
            startActivityForResult(intent, PICK_IMAGE_REQUEST_CODE);
        } else {
            Toast.makeText(this, "无法打开相机", Toast.LENGTH_SHORT).show();
        }
    }

    // 处理返回的结果（文件选择或拍照）
    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);

        if (resultCode == RESULT_OK) {
            if (requestCode == PICK_FILE_REQUEST_CODE) {
                // 用户选择了文件
                Uri fileUri = data.getData();
                Toast.makeText(this, "文件选择成功: " + fileUri.toString(), Toast.LENGTH_SHORT).show();
            } else if (requestCode == PICK_IMAGE_REQUEST_CODE) {
                // 用户拍照并返回图片
                if (data != null) {
                    Uri imageUri = data.getData();
                    if (imageUri != null) {
                        Toast.makeText(this, "图片拍摄成功: " + imageUri.toString(), Toast.LENGTH_SHORT).show();
                    }
                }
            }
        } else {
            Toast.makeText(this, "操作取消或失败", Toast.LENGTH_SHORT).show();
        }
    }
}
