package com.dreamteam.hackupc2017.dostuff.Providers;


import com.dreamteam.hackupc2017.dostuff.Network.Activity;
import com.dreamteam.hackupc2017.dostuff.Network.NetworkModule;

import java.util.ArrayList;
import java.util.List;

import io.reactivex.Single;
import io.reactivex.android.schedulers.AndroidSchedulers;
import io.reactivex.schedulers.Schedulers;

public class EventProvider {
    public Single<List<Event>> getAllEvents(int userid) {
        return NetworkModule.getInstance(null).getActivities()
                .flattenAsFlowable(list -> list)
                .flatMap(activity ->
                        NetworkModule.getInstance(null).getLikes(activity.Id).map(likes ->
                                new Event(activity, likes)).toFlowable())
                .subscribeOn(Schedulers.io())
                .observeOn(AndroidSchedulers.mainThread())
                .toList();
    }
}
