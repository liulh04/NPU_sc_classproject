package com.example.taskhelpapp;

import android.content.Intent;
import android.os.Bundle;
import android.widget.Button;

import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {

    private Button publishTaskButton;
    private Button helpTaskButton;
    private Button profileButton;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        publishTaskButton = findViewById(R.id.publish_task_button);
        helpTaskButton = findViewById(R.id.help_task_button);
        profileButton = findViewById(R.id.profile_button);

        publishTaskButton.setOnClickListener(v -> openPublishTaskPage());
        helpTaskButton.setOnClickListener(v -> openHelpTaskPage());
        profileButton.setOnClickListener(v -> openProfilePage());
    }

    private void openPublishTaskPage() {
        Intent intent = new Intent(this, PublishTaskActivity.class);
        startActivity(intent);
    }

    private void openHelpTaskPage() {
        Intent intent = new Intent(this, HelpTaskActivity.class);
        startActivity(intent);
    }

    private void openProfilePage() {
        Intent intent = new Intent(this, ProfileActivity.class);
        startActivity(intent);
    }
}
