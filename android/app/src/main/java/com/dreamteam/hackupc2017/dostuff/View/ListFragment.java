package com.dreamteam.hackupc2017.dostuff.View;

import android.os.Bundle;
import android.support.constraint.ConstraintLayout;
import android.support.design.widget.BottomSheetBehavior;
import android.support.design.widget.FloatingActionButton;
import android.support.design.widget.Snackbar;
import android.support.v4.app.Fragment;
import android.support.v4.widget.SwipeRefreshLayout;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.TextView;

import com.dreamteam.hackupc2017.dostuff.Adapters.EventAdapter;
import com.dreamteam.hackupc2017.dostuff.Network.NetworkModule;
import com.dreamteam.hackupc2017.dostuff.Presenters.ListPresenter;
import com.dreamteam.hackupc2017.dostuff.Providers.Event;
import com.dreamteam.hackupc2017.dostuff.R;
import com.jakewharton.rxbinding2.view.RxView;

import java.util.List;

import butterknife.BindView;
import butterknife.ButterKnife;
import butterknife.Unbinder;
import io.reactivex.Completable;
import io.reactivex.Single;
import io.reactivex.android.schedulers.AndroidSchedulers;
import io.reactivex.schedulers.Schedulers;

import static com.dreamteam.hackupc2017.dostuff.Adapters.EventAdapter.MY_ID;


public class ListFragment extends Fragment implements BaseView, SwipeRefreshLayout.OnRefreshListener {

    @BindView(R.id.event_list) RecyclerView eventList;
    @BindView(R.id.main_frame) ConstraintLayout mainFrame;
    @BindView(R.id.floatingActionButton) FloatingActionButton fab;
    @BindView(R.id.bottom_sheet) LinearLayout llBottomSheet;
    @BindView(R.id.clear) FloatingActionButton cancel;
    @BindView(R.id.submit) FloatingActionButton submit;
    @BindView(R.id.new_activity_name) EditText newActivityName;
    @BindView(R.id.new_activity_description) EditText newActivityDescription;
    @BindView(R.id.drawer_layout) SwipeRefreshLayout swipeRefreshLayout;

    Unbinder unbinder;

    EventAdapter adapter;
    ListPresenter presenter;

    BottomSheetBehavior bottomSheetBehavior;

    public ListFragment() {
        // Required empty public constructor
    }

    public static ListFragment newInstance() {
        ListFragment fragment = new ListFragment();
        return fragment;
    }

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        // Inflate the layout for this fragment
        View view = inflater.inflate(R.layout.fragment_list_root, container, false);
        unbinder = ButterKnife.bind(this, view);
        LinearLayoutManager llm = new LinearLayoutManager(getContext());
        llm.setOrientation(LinearLayoutManager.VERTICAL);
        adapter = new EventAdapter(getContext(), eventList);
        eventList.setLayoutManager(llm);
        eventList.setAdapter(adapter);

        presenter = new ListPresenter();
        presenter.attachView(this);
        presenter.loadEvents();

        bottomSheetBehavior = BottomSheetBehavior.from(llBottomSheet);
        bottomSheetBehavior.setHideable(true);
        RxView.clicks(fab).subscribe(action ->
                bottomSheetBehavior.setState(BottomSheetBehavior.STATE_EXPANDED));

        RxView.clicks(cancel).subscribe(o ->
                bottomSheetBehavior.setState(BottomSheetBehavior.STATE_COLLAPSED));
        RxView.clicks(submit).subscribe((v) -> {
            if (!newActivityName.getText().toString().equals("")) {
                bottomSheetBehavior.setState(BottomSheetBehavior.STATE_COLLAPSED);
                NetworkModule.getInstance(null).addActivity(MY_ID,
                        "Igor Kholopov", newActivityName.getText().toString(),
                        newActivityDescription.getText().toString())
                        .subscribeOn(Schedulers.io())
                        .observeOn(AndroidSchedulers.mainThread())
                        .flatMap((a) -> refresh()).subscribe((a) -> {

                        },
                        error -> showError(error.getMessage()));
            } else {
                showError("Please enter a title");
            }

    });
        swipeRefreshLayout.setOnRefreshListener(this);
        return view;
    }

    @Override
    public void onDestroy() {
        super.onDestroy();
        presenter.detachView();
        unbinder.unbind();
    }

    @Override
    public void showError(String errorMessage) {
        Snackbar.make(mainFrame, errorMessage, Snackbar.LENGTH_SHORT).show();
    }

    public void onBack() {
        bottomSheetBehavior.setState(BottomSheetBehavior.STATE_COLLAPSED);
    }


    public void setEvents(List<Event> events) {
        adapter.updateEventsList(events);
        adapter.notifyDataSetChanged();
    }

    public Single<List<Event>> refresh() {
        return presenter.loadEvents();
    }

    @Override
    public void onRefresh() {
        this.refresh()
                .doOnError((e) ->  {
                    this.showError(e.getMessage());
                    swipeRefreshLayout.setRefreshing(false);
                })
                .subscribe((a) -> {
            swipeRefreshLayout.setRefreshing(false);
        }, error -> {
            this.showError(error.getMessage());
            swipeRefreshLayout.setRefreshing(false);
        });
    }
}
