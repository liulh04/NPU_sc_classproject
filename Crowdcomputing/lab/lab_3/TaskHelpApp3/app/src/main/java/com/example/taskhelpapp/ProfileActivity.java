package com.example.taskhelpapp;

import android.os.Bundle;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

public class ProfileActivity extends AppCompatActivity {

    private TextView userInfoTextView;
    private Button backButton;
    private Button saveButton;
    private EditText userInfoEditText;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_profile);

        userInfoTextView = findViewById(R.id.user_info_text);
        userInfoEditText = findViewById(R.id.edit_user_info);
        saveButton = findViewById(R.id.save_button);
        backButton = findViewById(R.id.back_button);

        // 显示个人信息
        String userInfo = "姓名: 张三\n年龄: 25\n职业: 程序员\n账号ID: 123456";
        userInfoTextView.setText(userInfo);

        saveButton.setOnClickListener(v -> saveProfile());
        backButton.setOnClickListener(v -> finish());
    }

    private void saveProfile() {
        // 获取修改的资料
        String updatedInfo = userInfoEditText.getText().toString();
        userInfoTextView.setText(updatedInfo); // 更新显示的资料
        Toast.makeText(this, "资料已保存", Toast.LENGTH_SHORT).show();
    }
}
