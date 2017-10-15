package com.dreamteam.hackupc2017.dostuff.Adapters;


import android.animation.ValueAnimator;
import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.support.annotation.NonNull;
import android.support.constraint.ConstraintLayout;
import android.support.transition.TransitionManager;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.TextView;

import com.dreamteam.hackupc2017.dostuff.Network.Like;
import com.dreamteam.hackupc2017.dostuff.Network.NetworkModule;
import com.dreamteam.hackupc2017.dostuff.Providers.Event;
import com.dreamteam.hackupc2017.dostuff.R;
import com.jakewharton.rxbinding2.view.RxView;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import butterknife.BindView;
import butterknife.ButterKnife;
import io.reactivex.android.schedulers.AndroidSchedulers;
import io.reactivex.disposables.CompositeDisposable;
import io.reactivex.disposables.Disposable;
import io.reactivex.schedulers.Schedulers;
import okhttp3.HttpUrl;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;

public class EventAdapter extends RecyclerView.Adapter<EventAdapter.EventViewHolder> {

    private List<Event> events;
    private List<Event> allEevents;
    private Context context;
    private RecyclerView recyclerView;

    public static long MY_ID = 121296547;

    private int expandedPosition = -1;

    public EventAdapter(Context context, RecyclerView recyclerView) {
        this.context = context;
        this.recyclerView = recyclerView;
        setHasStableIds(true);
    }

    @Override
    public long getItemId(int position) {
        return position;
    }

    @Override
    public EventViewHolder onCreateViewHolder(ViewGroup parent, int viewType) {
        View view = LayoutInflater.from(parent.getContext()).inflate(R.layout.event_card, parent,
                false);
        EventViewHolder viewHolder = new EventViewHolder(view, context);
        return viewHolder;
    }

    @Override
    public void onBindViewHolder(EventViewHolder holder, int position) {
        holder.name.setText(events.get(position).Title);
        holder.image.setImageBitmap(null);
        Bitmap local = loadLocal(events.get(position).Title);
        if(local == null) {
            holder.disposable.add(NetworkModule.getInstance(null).getIcon(events.get(position).Title).map(response -> {
                if (response.images.size() != 0) {
                    HttpUrl httpUrl = HttpUrl.parse(response.images.get(0).ThumbnailUrl);
                    return fetchImage(httpUrl);
                }
                return null;
            }).subscribeOn(Schedulers.io()).observeOn(AndroidSchedulers.mainThread())
                    .subscribe(bitmap -> {
                        FileOutputStream stream = new FileOutputStream(new File(context.getFilesDir(), events.get(position).Title));
                        bitmap.compress(Bitmap.CompressFormat.PNG, 100, stream);
                        stream.flush();
                        stream.close();
                        holder.image.setImageBitmap(bitmap);
                    }, error -> {
                        Log.e("EventAdapter", error.getMessage());
                    }));
        } else {
            holder.image.setImageBitmap(local);
        }
        boolean expanded = position == expandedPosition;
        showDetails(holder, expanded, events.get(position));
        RxView.clicks(holder.itemView).subscribe((o) -> {
            int oldPosition = expandedPosition;
            expandedPosition = expanded ? -1 : position;
            notifyItemChanged(position);
            if(oldPosition != -1) {
                notifyItemChanged(oldPosition);
            }
        });
        boolean liked = isLiked(events.get(position).Likes);
        if(liked) {
            holder.likeButton.setBackgroundColor(context.getResources().getColor(R.color.selectedButton));
            holder.likeButton.setCompoundDrawablesWithIntrinsicBounds(context.getResources().getDrawable(R.drawable.ic_heart_full),
                    null, null, null);
        } else {
            holder.likeButton.setBackgroundColor(context.getResources().getColor(R.color.colorPrimary));
            holder.likeButton.setCompoundDrawablesWithIntrinsicBounds(context.getResources().getDrawable(R.drawable.ic_heart_empty),
                    null, null, null);
        }
        holder.likeButton.setText(String.valueOf(events.get(position).Likes.size()));
        holder.likeButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if(!liked) {
                    holder.disposable.add(NetworkModule.getInstance(null).addLike(events.get(position).Id, MY_ID, "Igor Kholopov")
                            .flatMap(status -> NetworkModule.getInstance(null).getLikes(events.get(position).Id))
                            .subscribeOn(Schedulers.io())
                            .observeOn(AndroidSchedulers.mainThread())
                            .subscribe(likes -> {
                                events.get(position).Likes = likes;
                                holder.likeAdapter.updateLikes(likes);
                                holder.likeButton.setBackgroundColor(context.getResources().getColor(R.color.selectedButton));
                                holder.likeButton.setCompoundDrawablesWithIntrinsicBounds(context.getResources().getDrawable(R.drawable.ic_heart_full),
                                        null, null, null);
                                notifyItemChanged(position);
                            }));
                } else {
                    holder.disposable.add(NetworkModule.getInstance(null).removeLike(events.get(position).Id, MY_ID)
                            .flatMap(status -> NetworkModule.getInstance(null).getLikes(events.get(position).Id))
                            .subscribeOn(Schedulers.io())
                            .observeOn(AndroidSchedulers.mainThread())
                            .subscribe(likes -> {
                                events.get(position).Likes = likes;
                                holder.likeAdapter.updateLikes(likes);
                                holder.likeButton.setBackgroundColor(context.getResources().getColor(R.color.colorPrimary));
                                holder.likeButton.setCompoundDrawablesWithIntrinsicBounds(context.getResources().getDrawable(R.drawable.ic_heart_empty),
                                        null, null, null);
                                notifyItemChanged(position);
                            }));
                }
            }
        });
    }

    private Bitmap loadLocal(String title) {
        try {
            return BitmapFactory.decodeStream(new FileInputStream(new File(context.getFilesDir(), title)));
        } catch (FileNotFoundException e) {
            return null;
        }
    }

    @Override
    public int getItemCount() {
        if(events == null) {
            return 0;
        }
        return events.size();
    }

    public void updateEventsList(@NonNull List<Event> events) {
        this.allEevents = events;
        this.events = allEevents;
    }

    static class EventViewHolder extends RecyclerView.ViewHolder {

        @BindView(R.id.event_name) TextView name;
        @BindView(R.id.icon) ImageView image;
        @BindView(R.id.details) RecyclerView details;
        @BindView(R.id.main_frame) ConstraintLayout mainFrame;
        @BindView(R.id.like_button) Button likeButton;
        View itemView;
        LikeAdapter likeAdapter;

        CompositeDisposable disposable = new CompositeDisposable();

        EventViewHolder(View itemView, Context context) {
            super(itemView);
            likeAdapter = new LikeAdapter(context);
            this.itemView = itemView;
            ButterKnife.bind(this, itemView);
        }
    }

    private Bitmap fetchImage(HttpUrl url) {
        OkHttpClient client = new OkHttpClient.Builder().cache(NetworkModule.getInstance(null).cache)
                .build();
        try {
            Response response = client.newCall(new Request.Builder().url(url).build()).execute();
            if (response.isSuccessful()) {
                return BitmapFactory.decodeStream(response.body().byteStream());
            } else if (!response.isSuccessful()) {
                Log.e("ProfilePresenter", response.body().string());
                return null;
            }
        } catch (IOException e) {
            Log.e("ProfilePresenter", e.getMessage());
            return null;
        }

        return null;
    }

    private void showDetails(EventViewHolder holder, boolean expanded, Event event) {
        holder.details.setVisibility(expanded ? View.VISIBLE : View.GONE);
        if(expanded) {
            LinearLayoutManager llm = new LinearLayoutManager(context);
            llm.setOrientation(LinearLayoutManager.VERTICAL);
            holder.details.setLayoutManager(llm);
            holder.details.setAdapter(holder.likeAdapter);
            holder.likeAdapter.updateLikes(event.Likes);
        }
    }

    private boolean isLiked(List<Like> likes) {
        boolean liked = false;
        for (Like like : likes) {
            if(like.PersonId == MY_ID) {
                liked = true;
                break;
            }
        }
        return liked;
    }
}
