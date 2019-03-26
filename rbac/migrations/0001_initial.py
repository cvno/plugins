# Generated by Django 2.1.7 on 2019-03-26 18:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(max_length=32, verbose_name='操作标题')),
                ('code', models.CharField(max_length=32, verbose_name='方法')),
            ],
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(max_length=32, verbose_name='菜单名称')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='p', to='rbac.Menu', verbose_name='父菜单')),
            ],
        ),
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(max_length=32, verbose_name='权限')),
                ('url', models.CharField(max_length=128, verbose_name='URL正则')),
                ('status', models.BooleanField(verbose_name='是否显示菜单')),
                ('menu', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='permissions', to='rbac.Menu', verbose_name='所属菜单')),
            ],
        ),
        migrations.CreateModel(
            name='Permission2Action2Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='permissions', to='rbac.Action', verbose_name='操作')),
                ('permission', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='actions', to='rbac.Permission', verbose_name='权限URL')),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(max_length=32, verbose_name='角色')),
                ('level', models.IntegerField(default=0, verbose_name='level 标识')),
            ],
        ),
        migrations.CreateModel(
            name='User2Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='users', to='rbac.Role', verbose_name='角色')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='roles', to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
        ),
        migrations.AddField(
            model_name='permission2action2role',
            name='role',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='p2as', to='rbac.Role', verbose_name='角色'),
        ),
        migrations.AlterUniqueTogether(
            name='permission2action2role',
            unique_together={('permission', 'action', 'role')},
        ),
    ]
