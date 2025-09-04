package com.example.taskhelpapp;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.CheckBox;
import android.widget.TextView;

import java.util.ArrayList;

public class TaskAdapter extends android.widget.BaseAdapter {

    private Context context;
    private ArrayList<Task> tasks;

    public TaskAdapter(Context context, ArrayList<Task> tasks) {
        this.context = context;
        this.tasks = tasks;
    }

    @Override
    public int getCount() {
        return tasks.size();
    }

    @Override
    public Object getItem(int position) {
        return tasks.get(position);
    }

    @Override
    public long getItemId(int position) {
        return position;
    }

    @Override
    public View getView(int position, View convertView, ViewGroup parent) {
        if (convertView == null) {
            convertView = LayoutInflater.from(context).inflate(R.layout.task_item_layout, parent, false);
        }

        Task task = tasks.get(position);

        TextView taskTitleTextView = convertView.findViewById(R.id.task_title);
        TextView taskDescriptionTextView = convertView.findViewById(R.id.task_description);
        TextView taskLocationTextView = convertView.findViewById(R.id.task_location);
        CheckBox taskCheckBox = convertView.findViewById(R.id.task_checkbox);

        taskTitleTextView.setText(task.getTitle());
        taskDescriptionTextView.setText(task.getDescription());
        taskLocationTextView.setText(task.getLocation());

        taskCheckBox.setChecked(false); // 默认不选中

        return convertView;
    }
}
