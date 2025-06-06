# Generated by Django 5.0.7 on 2024-11-02 09:44

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(blank=True, max_length=150, unique=True, verbose_name='email')),
                ('username', models.CharField(blank=True, max_length=150, unique=True, verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, null=True, verbose_name='first_name')),
                ('last_name', models.CharField(blank=True, max_length=150, null=True, verbose_name='last_name')),
                ('is_online', models.BooleanField(default=False, verbose_name='is_online')),
                ('country', models.CharField(blank=True, max_length=100, null=True)),
                ('city', models.CharField(blank=True, max_length=100, null=True)),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('zip_code', models.CharField(blank=True, max_length=20, null=True)),
                ('picture', models.CharField(blank=True, max_length=150, null=True, verbose_name='pic')),
                ('background_picture', models.CharField(blank=True, max_length=150, null=True, verbose_name='back pic')),
                ('rank', models.IntegerField(default=0, verbose_name='Rank')),
                ('wins', models.IntegerField(default=0, verbose_name='wins')),
                ('loses', models.IntegerField(default=0, verbose_name='loses')),
                ('isSettings', models.BooleanField(default=False, verbose_name='isSettings')),
                ('isInviting', models.BooleanField(default=False, verbose_name='isInviting')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created_at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated_at')),
                ('badge', models.CharField(choices=[('BRONZE', 'Bronze'), ('SILVER', 'Silver'), ('GOLD', 'Gold'), ('PLATINUM', 'Platinum'), ('DIAMOND', 'Diamond'), ('HEROIC', 'Heroic'), ('GRAND_MASTER', 'Grand Master')], default='BRONZE', max_length=15)),
                ('play_requests', models.ManyToManyField(blank=True, related_name='received_play_requests', to='prfl.profile')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('from_user', models.CharField(max_length=150)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created_at')),
                ('notification_type', models.CharField(choices=[('FRIENDSHIP_REQUEST', 'Friendship request'), ('HANDLE_REQUESTED_FRIENDSHIP', 'Handle request friendship'), ('PLAYWITHME_REQUEST', 'PlayWithMe request'), ('JOINING_TOURNAMENT', 'Joining Tournament'), ('TOURNAMENT_REMINDER', 'Tournament reminder')], default='FRIENDSHIP_REQUEST', max_length=50)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='prfl.profile')),
            ],
            options={
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='FriendRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('from_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_requests', to='prfl.profile')),
                ('to_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_requests', to='prfl.profile')),
            ],
            options={
                'unique_together': {('from_user', 'to_user')},
            },
        ),
        migrations.CreateModel(
            name='Friend',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('friend', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friend_of', to='prfl.profile')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='my_friend', to='prfl.profile')),
            ],
            options={
                'unique_together': {('profile', 'friend')},
            },
        ),
        migrations.CreateModel(
            name='BlockedFriend',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('blocked_friend', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blocker', to='prfl.profile')),
                ('blocker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blocked', to='prfl.profile')),
            ],
            options={
                'unique_together': {('blocker', 'blocked_friend')},
            },
        ),
    ]
