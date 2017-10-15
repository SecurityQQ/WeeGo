package com.dreamteam.hackupc2017.dostuff.View;

import android.os.Bundle;
import android.support.design.widget.FloatingActionButton;
import android.support.design.widget.Snackbar;
import android.support.v4.widget.SwipeRefreshLayout;
import android.view.MenuInflater;
import android.view.View;
import android.support.design.widget.NavigationView;
import android.support.v4.view.GravityCompat;
import android.support.v4.widget.DrawerLayout;
import android.support.v7.app.ActionBarDrawerToggle;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.view.Menu;
import android.view.MenuItem;

import com.dreamteam.hackupc2017.dostuff.Network.NetworkModule;
import com.dreamteam.hackupc2017.dostuff.R;

import butterknife.BindView;
import butterknife.ButterKnife;

public class MainActivity extends AppCompatActivity {

    private static final String MAIN_FRAGMENT = "MAIN_FRAGMENT";

    @BindView(R.id.toolbar) Toolbar toolbar;

    ListFragment fragment;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        ButterKnife.bind(this);
        if(savedInstanceState == null) {
            fragment = new ListFragment();
            getSupportFragmentManager().beginTransaction().add(R.id.container, fragment, MAIN_FRAGMENT).commit();
        }
        setSupportActionBar(toolbar);
    }



    @Override
    public void onBackPressed() {
        if(fragment == null) {
            return;
        }
        fragment.onBack();
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        MenuInflater inflater = getMenuInflater();
        inflater.inflate(R.menu.options_menu, menu);

        return true;
    }
}
