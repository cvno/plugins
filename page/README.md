# 分页
- 自定义一个页面显示多少页码
- 如果获取到异常页码参数则设置为第一页
- 视图函数需要把生成的`html`代码传给模板

## 目录
- [样式依赖](#样式依赖)
- [CDN](#CDN)
- [\__init__](#\__init__)
- [pager](#pager)
- [使用](#使用)
- [模板代码](#模板代码)

## 样式依赖
- ([Bootstrap](http://v3.bootcss.com/css/))

## CDN

```html
<link href="http://cdn.bootcss.com/bootstrap/4.0.0-alpha.6/css/bootstrap.min.css" rel="stylesheet">
```

### \__init__
- 如果出现除不尽的则给总的页数加1
- 如果转换页码出现错误,则把当前页码设置为第1页

```python
def __init__(self, current_page, all_count, per_page, base_url, show_page=11):
    '''
    :param current_page:     当前的页码
    :param all_count:        总的页码
    :param per_page:         每页显示几条数据
    :param base_url:         生成页码的地址
    :param show_page:        显示的页数
    '''
       try:
            if current_page == None:
                # 如果没有获取到当前的页码,则把当前页码设置为1
                self.current_page = 1
            else:
                # 否则把获取到的参数强转为 int
                self.current_page = int(current_page)
            self.per_page = per_page    # 每页显示几条数据
        except Exception as e:
            self.current_page = 1
        # 计算需要的页数
        a,b = divmod(all_count,per_page)
        if b:
            a += 1
        self.all_pager = a          # 总的页数
        self.show_page = show_page  # 显示的页数
        self.base_url = base_url    # url
```

## pager
>生成页码的 html

## 使用

``` python
# 使用的时候实例化
page_info = PageInfo(request.GET.get('page'),all_count, 3, '/index.html')
```
## 模板代码

```
{% if page_info.pager %}
    <div class="container text-center">
        <div class="col-md-8">
            <nav aria-label="Page navigation center">
                  <ul class="pagination">
                      {{ page_info.pager|safe }}
                  </ul>
            </nav>
        </div>
    </div>
{% endif %}
```


