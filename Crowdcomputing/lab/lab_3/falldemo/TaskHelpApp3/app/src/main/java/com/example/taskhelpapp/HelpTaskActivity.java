package com.example.taskhelpapp;

import android.content.SharedPreferences;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;
import android.content.Intent;

import androidx.appcompat.app.AppCompatActivity;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.Set;

public class HelpTaskActivity extends AppCompatActivity {

    private ListView taskListView;
    private ArrayList<Task> tasks = new ArrayList<>();
    private TaskAdapter adapter;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_help_task);

        taskListView = findViewById(R.id.task_list_view);

        // 从SharedPreferences加载任务列表
        loadTasks();

        // 使用自定义适配器展示任务列表
        adapter = new TaskAdapter(HelpTaskActivity.this, tasks);
        taskListView.setAdapter(adapter);
    }

    // 从SharedPreferences加载任务
    private void loadTasks() {
        SharedPreferences sharedPreferences = getSharedPreferences("TaskData", MODE_PRIVATE);
        Set<String> tasksSet = sharedPreferences.getStringSet("tasks", new HashSet<>());
        for (String taskData : tasksSet) {
            String[] taskDetails = taskData.split(" \\| ");
            if (taskDetails.length == 3) {
                tasks.add(new Task(taskDetails[0], taskDetails[1], taskDetails[2]));
            }
        }
    }

    // 自定义适配器，确保每一项任务都有一个“帮助”按钮
    private class TaskAdapter extends ArrayAdapter<Task> {

        public TaskAdapter(HelpTaskActivity context, ArrayList<Task> tasks) {
            super(context, R.layout.task_item, tasks);
        }

        @Override
        public View getView(int position, View convertView, ViewGroup parent) {
            if (convertView == null) {
                convertView = LayoutInflater.from(getContext()).inflate(R.layout.task_item, parent, false);
            }

            Task currentTask = getItem(position);

            // 获取任务标题和按钮
            TextView taskTitle = convertView.findViewById(R.id.task_title);
            Button helpButton = convertView.findViewById(R.id.help_button);

            taskTitle.setText(currentTask.getTitle());

            // 设置帮助按钮的点击事件
            helpButton.setOnClickListener(v -> {
                // 显示一个Toast提示用户选择的任务
                Toast.makeText(HelpTaskActivity.this, "您选择了任务: " + currentTask.getTitle(), Toast.LENGTH_SHORT).show();

                // 启动 HelpTaskDetailActivity 并传递任务信息
                Intent intent = new Intent(HelpTaskActivity.this, HelpTaskDetailActivity.class);
                intent.putExtra("taskTitle", currentTask.getTitle());
                intent.putExtra("taskDescription", currentTask.getDescription());
                intent.putExtra("taskLocation", currentTask.getLocation());
                startActivity(intent); // 启动目标 Activity
            });

            return convertView;
        }
    }
}
