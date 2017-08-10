# 验证码
>生成验证码的时候,可以使用一些字体

- [url](#url)
- [view](#view)
- [模板](#模板)

## 依赖

```python
from io import BytesIO
```
- 字体

## 使用
### url

```python
url(r'^check_code/', account.check_code),
```

### view

```python
# 导入
from io import BytesIO
from utlis.random_check_code import  rd_check_code

def check_code(request):
    img,code = rd_check_code()
    stream = BytesIO()
    img.save(stream,'png')
    request.session['code'] = code
    return HttpResponse(stream.getvalue())
```

### 模板
> 添加的单击事件是更新验证码

```html
<img onclick="changeSrc(this);" src="/check_code/" alt="验证码">
```

```javascript
// 刷新/更新验证码
function changeSrc(ths) {
            ths.src = ths.src + '?';
        }
```

