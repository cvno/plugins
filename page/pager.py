class PageInfo(object):
    def __init__(self, current_page, all_count, per_page, base_url, show_page=11):
        try:
            if current_page == None:
                self.current_page = 1
            else:
                self.current_page = int(current_page)
            self.per_page = per_page
        except Exception as e:
            self.current_page = 1
        # 计算需要的页数
        a,b = divmod(all_count,per_page)
        print(a,b)
        if b:
            a += 1
            print(a)
        self.all_pager = a
        print(self.all_pager)
        self.show_page = show_page  # 显示的页数
        self.base_url = base_url

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
            first = "<li class='disabled'><a href='javascript:;'>首页</a></li>"          # 首页
            prev = "<li class='disabled'><a href='javascript:;'><</a></li>"             # 上页
        else:
            first = "<li ><a href='%s?page=%s'>首页</a></li>" % (self.base_url, 1)
            prev = "<li><a href='%s?page=%s'>上一页</a></li>" % (self.base_url, self.current_page - 1)
        page_list.append(first)
        page_list.append(prev)

        # 页码
        for i in range(begin, stop+1):
            if i == self.current_page:
                temp = "<li class='active'><a href='javascript:;'>%s</a></li>"%i
            else:
                temp = "<li><a href='%s?page=%s'>%s</a></li>" % (self.base_url, i, i)
            page_list.append(temp)

        # 下一页
        if self.current_page >= self.all_pager:
            nex = "<li class='disabled'><a href='javascript:;'>></a>"
            last = "<li class='disabled'><a href='javascript:;'>尾页</a></li>"
        else:
            nex = "<li><a href='%s?page=%s'>></a></li>" % (self.base_url, self.current_page + 1)
            last = "<li><a href='%s?page=%s'>尾页</a></li>" % (self.base_url, self.all_pager)


        page_list.append(nex)
        page_list.append(last)

        if 1 == self.all_pager:
            return None

        return ''.join(page_list)