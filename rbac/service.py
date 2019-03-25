import re
from django.utils.safestring import mark_safe
from django.db.models import Count

from rbac import models

def permission_session(request):
    '''
    获取当前用户的所有权限信息
    {
        '/ah-index.html': ["GET", "POST", "DEL", "Edit"],
        '/order.html': ["GET", "POST", "DEL", "Edit"],
        '/index-(\d+).html': ["GET", "POST", "DEL", "Edit"],
    }
    :param request:
    :return:
    '''
    user = models.User.objects.get(id=request.user.id)

    # 当前用户的所有角色
    roles = models.Role.objects.filter(users__user=user)
    # 获取用户的最高等级
    last = None
    for role in roles:
        last = role
        if last != None and last.level <= role.level:
            last = role
    request.session['permission_name'] = last.caption if last else '未知用户'

    # 当前用户的所有权限(重复)+方法
    p2a = models.Permission2Action2Role.objects.filter(role__in=list(roles)).values('permission__url', "action__code")

    res = {}
    for item in p2a:
        if not res.get(item['permission__url']):
            res[item['permission__url']] = []
            res[item['permission__url']].append(item['action__code'])
        else:
            res[item['permission__url']].append(item['action__code'])
    print(res)
    return res


def menu(request):
    '''
    获取当前用户的菜单, 根据用户ID，当前URL:获取用户所有菜单以及权限，是否显示，是否打开
    '''

    # 当前用户信息
    user = models.User.objects.get(id=request.user.id)

    # 当前用户的所有角色
    roles = models.Role.objects.filter(users__user=user)

    # 当前用户的所有权限(重复)+方法
    p2a = models.Permission2Action2Role.objects.filter(role__in=list(roles)).values('permission__url', "action__code")

    user_permission_dict = {}

    for item in p2a:
        if item['permission__url'] in user_permission_dict:
            user_permission_dict[item['permission__url']].append(item['action__code'])
        else:
            user_permission_dict[item['permission__url']] = [item['action__code'], ]
    # 权限信息

    permission_list = models.Permission2Action2Role.objects.filter(role__in=roles).values('permission_id',
                                                                                          'permission__caption',
                                                                                          'permission__url',
                                                                                          'permission__status',
                                                                                          'permission__menu').annotate(c=Count('id'))
    all_menu_list = models.Menu.objects.values('id', 'caption', 'parent_id')

    # ------  结构化处理开始
    all_menu_dict = {}
    for row in all_menu_list:
        row['opened'] = False   # 菜单是否打开
        row['status'] = False   # 菜单是否显示
        row['child'] = []
        all_menu_dict[row['id']] = row

    for per in permission_list:
        item = {'id': per['permission__menu'], 'caption': per['permission__caption'], 'url': per['permission__url'],
                'parent_id': per['permission__menu'],
                'opened': False,
                'status': per['permission__status']}
        menu_id = item['parent_id']
        all_menu_dict[menu_id]['child'].append(item)
        if re.match(item['url'], request.path_info):
        # if re.match(r'/sound_(\d+).html', request.path_info):
            item['opened'] = True

        if item['opened']:
            pid = menu_id
            while not all_menu_dict[pid]['opened']:
                all_menu_dict[pid]['opened'] = True
                pid = all_menu_dict[pid]['parent_id']
                if not pid:
                    break

        if item['status']:
            pid = menu_id
            while not all_menu_dict[pid]['status']:
                all_menu_dict[pid]['status'] = True
                pid = all_menu_dict[pid]['parent_id']
                if not pid:
                    break

    result = []
    for row in all_menu_list:
        pid = row['parent_id']
        if pid:
            all_menu_dict[pid]['child'].append(row)
        else:
            result.append(row)

    def menu_tree(menu_list):
        tpl1 = """
        <!--Menu list item-->
        <li class="">
            <a href="#">
                <i class="psi-mouse-3"></i>
                <span class="menu-title">{0}</span>
                <i class="arrow"></i>
            </a>

            <!--Submenu-->
            <ul class="collapse {2}">
                {1}
            </ul>
        </li>
        """
        tpl2 = """
        <li class="{1}"><a href="{0}" >{2}</a></li>
        """
        menu_str = ""
        for menu in menu_list:
            if not menu['status']:  # 菜单不生成
                continue
            active = ""
            if menu['opened']:  # 菜单默认打开
                active = 'active-link'

            if menu.get('url'):
                menu_str += tpl2.format(menu['url'], active, menu['caption'])
            else:
                if menu.get('child'):
                    child = menu_tree(menu.get('child'))
                else:
                    child = ""
                menu_str += tpl1.format(menu['caption'], child, "in" if menu['opened'] else '')
        return menu_str


    menu_html = menu_tree(result)
    return mark_safe(menu_html)


# simple_tag
def css():
    v = """
        <style>
        .hide{
            display: none;
        }
        .menu-body{
            margin-left: 20px;
        }
        .menu-body a{
            display: block;
        }
        .menu-body a.active{
            color: red;
        }
    </style>
        """
    return v

# simple_tag
def js():
    v = """
        <script>
        $(function(){

            $('.menu-header').click(function(){
                $(this).next().removeClass('hide').parent().siblings().find('.menu-body').addClass('hide');

            })

        })
    </script>
    """
    return mark_safe(v)