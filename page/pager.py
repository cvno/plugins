from  urllib import parse
import urllib3


class PageInfo(object):
    def __init__(self, current_page, all_count, per_page, request, show_page=5):
        try:
            if current_page == None:
                self.current_page = 1
            else:
                self.current_page = int(current_page)
            self.per_page = per_page
        except Exception as e:
            self.current_page = 1
        # 计算需要的页数
        a,b = divmod(all_count, per_page)
        if b > 0:
            a += 1
        self.all_pager = a
        self.show_page = show_page  # 显示的页数
        self.base_url = request.get_full_path() # 获取 url及所有参数
        bits = list(parse.urlparse(self.base_url))
        qs =parse.parse_qs(bits[4]) # 把 url 中的参数转为 字典
        # 有参数就保留参数 但是 page 要去掉
        if qs:
            if qs.get('page'):  # 如果有 page 参数就删掉
                qs.pop('page')
                bits[4] = parse.urlencode(qs, True)
                mark = '&' if len(bits[4]) > 1 else '?'
                self.base_url = '{}{}'.format(parse.urlunparse(bits), mark)
            else:
                self.base_url = '{}&'.format(self.base_url)
        else:
            self.base_url = '{}?'.format(self.base_url)


    def start(self):
        return (self.current_page - 1) * self.per_page

    def end(self):
        return self.current_page * self.per_page

    def pager(self):
        page_list = []
        half = int((self.show_page - 1) / 2)  # 一共显示多少页码
        # 如果数据的总页数 < 11
        if self.all_pager < self.show_page:
            begin = 1
            stop = self.all_pager
        # 如果数据的总页数 > 11
        else:
            # 如果当前页 <= 5    永远显示 1,11
            if self.current_page <= half:
                begin = 1
                stop = self.show_page + 1
            else:
                if self.current_page + half > self.all_pager:
                    begin = self.all_pager - self.show_page + 1
                    stop = self.all_pager + 1
                else:
                    begin = self.current_page - half
                    stop = self.current_page + half + 1
        # begin = self.current_page - half        # 当前页的前几页
        # stop = self.current_page + half + 1     # 当前页的后几页

        # 上一页
        if self.current_page <= 1:
            first = "<li class='disabled'><a class='page-link' href='javascript:;'>首页</a></li>"          # 首页
            prev = "<li class='disabled'><a class='page-link' href='javascript:;'><</a></li>"             # 上页
        else:
            first = "<li class='page-item'><a href='{}page={}'>首页</a></li>".format(self.base_url, 1)
            prev = "<li class='page-item'><a class='page-link' href='{}page={}'><</a></li>".format(self.base_url, self.current_page -1)
        page_list.append(first)
        page_list.append(prev)

        # 页码
        for i in range(begin, stop):
            if i == self.current_page:
                temp = "<li class='page-item active'><a class='page-link' href='javascript:;'>{}</a></li>".format(i)
            else:
                temp = "<li class='page-item'><a class='page-link' href='{0}page={1}'>{1}</a></li>".format(self.base_url, i)
            page_list.append(temp)

        # 下一页
        if self.current_page >= self.all_pager:
            nex = "<li class='disabled page-item'><a class='page-link' href='javascript:;'>></a>"
            last = "<li class='disabled page-item'><a class='page-link' href='javascript:;'>尾页</a></li>"
        else:
            nex = "<li class='page-item'><a class='page-link' href='{}page={}'>></a></li>".format(self.base_url, self.current_page +1)
            last = "<li class='page-item'><a class='page-link' href='{}page={}'>尾页</a></li>".format(self.base_url, self.all_pager)


        page_list.append(nex)
        page_list.append(last)

        if 1 == self.all_pager:
            return None

        return ''.join(page_list)