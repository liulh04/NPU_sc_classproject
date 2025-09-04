package com.example.taskhelpapp;

import android.content.SharedPreferences;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.Set;

public class PublishTaskActivity extends AppCompatActivity {

    private EditText taskTitleEditText;
    private EditText taskDescriptionEditText;
    private EditText taskRangeEditText;
    private Button submitButton;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_publish_task);

        taskTitleEditText = findViewById(R.id.task_title);
        taskDescriptionEditText = findViewById(R.id.task_description);
        taskRangeEditText = findViewById(R.id.task_range);
        submitButton = findViewById(R.id.submit_button);

        submitButton.setOnClickListener(v -> publishTask());
    }

    private void publishTask() {
        String taskTitle = taskTitleEditText.getText().toString();
        String taskDescription = taskDescriptionEditText.getText().toString();
        String taskRange = taskRangeEditText.getText().toString();

        if (taskTitle.isEmpty() || taskDescription.isEmpty() || taskRange.isEmpty()) {
            Toast.makeText(this, "请填写完整任务信息", Toast.LENGTH_SHORT).show();
            return;
        }

        // 将任务保存到SharedPreferences
        SharedPreferences sharedPreferences = getSharedPreferences("TaskData", MODE_PRIVATE);
        SharedPreferences.Editor editor = sharedPreferences.edit();

        // 获取已存在的任务列表
        Set<String> tasksSet = sharedPreferences.getStringSet("tasks", new HashSet<>());
        tasksSet.add(taskTitle + " | " + taskDescription + " | " + taskRange);

        // 保存更新后的任务列表
        editor.putStringSet("tasks", tasksSet);
        editor.apply();

        // 任务发布后返回主界面
        Toast.makeText(this, "任务 '" + taskTitle + "' 发布成功!", Toast.LENGTH_SHORT).show();
        finish(); // 结束当前Activity，返回主界面
    }
}
