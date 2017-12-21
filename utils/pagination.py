#Author:Santi
from django.utils.safestring import mark_safe

class Page():
    def __init__(self, current_page, data_count, per_page_count=10, pager_num=7):
        self.current_page = current_page
        self.data_count = data_count
        self.per_page_count = per_page_count
        self.pager_num = pager_num

    @property
    def start(self):
        return (self.current_page-1) * self.per_page_count

    @property
    def end(self):
        return self.current_page * self.per_page_count

    @property
    def all_count(self):
        count, y = divmod(self.data_count, self.per_page_count)
        if y != 0:
            count += 1
        return count

    def page_str(self, base_url):
        page_str = []
        if self.all_count <= self.pager_num:
            start_index = 1
            end_index = self.pager_num + 1
        else:
            if self.current_page < self.pager_num:
                start_index = 1
                end_index = self.pager_num + 1
            elif self.current_page + (self.pager_num - 1) / 2 > self.all_count:
                start_index = self.all_count - self.pager_num
                end_index = self.all_count
            else:
                start_index = self.current_page - (self.pager_num - 1) / 2
                end_index = self.current_page + (self.pager_num + 1) / 2
        if self.current_page == 1:
            prev = "<a class='base' href='javascript:void(0);'>上一页</a>"
        else:
            prev = "<a class='base' href='%s?p=%s'>上一页</a>" % (base_url,self.current_page - 1)
        page_str.append(prev)
        for i in range(int(start_index), int(end_index)):
            if i == self.current_page:
                str = "<a class='base active' href='%s?p=%s'>%s</a>" % (base_url,i, i)
            else:
                str = "<a class='base' href='%s?p=%s'>%s</a>" % (base_url,i, i)
            page_str.append(str)
        if self.current_page == self.all_count:
            next = "<a class='base' href='javascript:void(0);'>下一页</a>"
        else:
            next = "<a class='base' href='%s?p=%s'>下一页</a>" % (base_url, self.current_page + 1)
        page_str.append(next)
        jump = '''
                <input type="text"><a id='a1' onclick='jump(this);'>GO</a>
                <script>
                    function jump(ths) {
                        var inp = ths.previousSibling
                        var val = inp.value
                        location.href = '%s' + val
                    }
                </script>
            ''' % base_url
        page_str.append(jump)
        page_str = "".join(page_str)
        page_str = mark_safe(page_str)
        return page_str

