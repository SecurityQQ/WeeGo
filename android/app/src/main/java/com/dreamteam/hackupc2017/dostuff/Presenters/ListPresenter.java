package com.dreamteam.hackupc2017.dostuff.Presenters;


import com.dreamteam.hackupc2017.dostuff.Providers.Event;
import com.dreamteam.hackupc2017.dostuff.Providers.EventProvider;
import com.dreamteam.hackupc2017.dostuff.View.ListFragment;

import java.util.List;

import io.reactivex.Completable;
import io.reactivex.Single;

public class ListPresenter extends BasePresenter<ListFragment> {

    EventProvider provider = new EventProvider();

    public Single<List<Event>> loadEvents() {
        Single<List<Event>> single = provider.getAllEvents(0);
        addDisposable(single.subscribe(events -> {
            bindedView.setEvents(events);
        }, error -> bindedView.showError(error.getMessage())));
        return single;
    }
}
