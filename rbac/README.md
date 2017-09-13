# rbac权限控制
>基于角色的权限控制

两大部分: `中间件`,`生成菜单 html`

### 使用方法：
    中间件：

    创建菜单：
        。。。

1.登录成功

```python
service.permission_session(1,request)
```

2.注册中间件

```python
rbac.middleware.md.RbacMiddleware 添加settings中MIDDLEWARE中，如：
    MIDDLEWARE = [
    ...
    'rbac.middleware.md.RbacMiddleware'
]
```

3.生产菜单(simple_tag)

```
service.menu(1,request.path_info)
    PS: 生成css/js使用simple_tag
```


