package com.dreamteam.hackupc2017.dostuff.Adapters;


import android.content.Context;
import android.content.Intent;
import android.net.Uri;
import android.support.v7.widget.RecyclerView;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.TextView;

import com.dreamteam.hackupc2017.dostuff.Network.Like;
import com.dreamteam.hackupc2017.dostuff.R;
import com.jakewharton.rxbinding2.view.RxView;

import java.util.List;

import butterknife.BindView;
import butterknife.ButterKnife;

public class LikeAdapter extends RecyclerView.Adapter<LikeAdapter.LikeViewHolder> {

    List<Like> likes;
    Context context;

    public LikeAdapter(Context context) {
        this.context = context;
    }

    @Override
    public LikeViewHolder onCreateViewHolder(ViewGroup parent, int viewType) {
        View view = LayoutInflater.from(parent.getContext()).inflate(R.layout.like_card, parent,
                false);
        LikeViewHolder viewHolder = new LikeViewHolder(view);
        return viewHolder;
    }

    @Override
    public void onBindViewHolder(LikeViewHolder holder, int position) {
        holder.name.setText(likes.get(position).PersonName);
        holder.name.setOnClickListener(view -> {
            String url = "tg://resolve?domain=" + likes.get(position).PersonUsername.substring(1);
            Intent intent = new Intent(Intent.ACTION_VIEW);
            intent.setData(Uri.parse(url));
            context.startActivity(intent);
        });
        holder.arrow.setOnClickListener(view -> {
            String url = "tg://resolve?domain=" + likes.get(position).PersonUsername.substring(1);
            Intent intent = new Intent(Intent.ACTION_VIEW);
            intent.setData(Uri.parse(url));
            context.startActivity(intent);
        });

    }

    @Override
    public int getItemCount() {
        if(likes == null) {
            return 0;
        }
        return likes.size();
    }

    public void updateLikes(List<Like> likes) {
        this.likes = likes;
        notifyDataSetChanged();
    }

    static class LikeViewHolder extends RecyclerView.ViewHolder {
        @BindView(R.id.like_name) TextView name;
        @BindView(R.id.arrow) ImageView arrow;

        public LikeViewHolder(View itemView) {
            super(itemView);
            ButterKnife.bind(this, itemView);
        }
    }
}
