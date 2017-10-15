package com.dreamteam.hackupc2017.dostuff.Presenters;



import android.util.Log;

import com.dreamteam.hackupc2017.dostuff.View.BaseView;

import io.reactivex.disposables.CompositeDisposable;
import io.reactivex.disposables.Disposable;

public abstract class BasePresenter<V extends BaseView> {
    private CompositeDisposable disposable;

    protected V bindedView;

    public void attachView(V view) {
        this.bindedView = view;
        if(disposable == null) {
            disposable = new CompositeDisposable();
        }
        disposable.clear();
    }

    public void detachView() {
        this.bindedView = null;
        disposable.clear();
    }

    public void onError(Throwable throwable) {
        String message = throwable.getMessage();
        Log.e("BasePresenter", message);
        if(bindedView != null) {
            bindedView.showError(message);
        }
    }

    public void addDisposable(Disposable disposable) {
        this.disposable.add(disposable);
    }
}

