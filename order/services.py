from common.utils import SQLUtils
from .models import OrderStatus, DetailOrder, Order

def get_profit_of_user(user, filter_date_begin=None, filter_date_end=None, order_status=None, sort_date_cond='asc'):
    base_sql = '''
        {select}
        from `order` join `detail_order` `d_o` join `merchandise` `m` join `history_order_status` `h`
            on `order`.`id` = `d_o`.`id_order` 
                AND `d_o`.`id_merchandise` = `m`.`id`
                AND `h`.`id_order` = `order`.`id`
        {where}
        {group}
        {order};
    '''
    sqlutils = SQLUtils()
    select_clause = ''' select `order`.`created_date` as `id`, sum(`d_o`.`total_price_after_discount`) `profit` '''

    sqlutils.add_where('`m`.`id_user` = %s', user)
    if order_status != None:
        sqlutils.add_where('`h`.`id_order_status` = %s', order_status)
    if filter_date_begin != None or filter_date_end != None:
        sqlutils.add_where('DATE(`order`.`created_date`) >= %s AND DATE(`order`.`created_date`) <= %s', [filter_date_begin, filter_date_end])

    group_clause = ''' group by DATE(`order`.`created_date`) '''
    sqlutils.add_order('`order`.`created_date` ' + sort_date_cond)

    income = Order.objects.raw(base_sql.format(select=select_clause, where=sqlutils.get_where_clause(), 
                                                group=group_clause, order=sqlutils.get_order_clause()),
                                sqlutils.get_params())
    return income

def count_status_order(user):
    count = OrderStatus.objects.raw('''
        SELECT `order_status`.`id`, `order_status`.`name`, 
            CASE
                WHEN `count` THEN `count`
                ELSE 0
            END AS `count`
        FROM `order_status` LEFT JOIN (
            SELECT (SELECT `tb1`.`id_order_status` 
                    FROM `history_order_status` `tb1`
                    WHERE `tb1`.`id_order` = `order`.`id`
                    ORDER BY tb1.`id` DESC
                    LIMIT 1) AS `id_order_status`, COUNT(DISTINCT `order`.`id`) `count`
            FROM `order`, `detail_order`, `merchandise`
            WHERE
                `order`.`id` = `detail_order`.`id_order` AND 
                `detail_order`.`id_merchandise` = `merchandise`.`id` AND
                `merchandise`.`id_user` = %s
            GROUP BY `id_order_status`
            ORDER BY `id_order_status`) AS `order_his`
        ON `order_status`.`id` = `order_his`.`id_order_status`;
    ''', [user])

    return count

def get_product_income_rank(user):
    income_rank = DetailOrder.objects.raw('''
        select `m`.`id`, `book`.`name`, `image`.`url`, sum(`d_o`.`total_price_after_discount`) `income`, sum(`d_o`.`quantity`) `count`
        from `order` join  `detail_order` `d_o` join `merchandise` `m` join `merchandise_image` `mi` join `book` join `image` 
        where `order`.`id` = `d_o`.`id_order` and `d_o`.`id_merchandise` = `m`.`id` and `m`.`id` = `mi`.`id_merchandise` and `mi`.`id_image` = `image`.`id` 
            and `m`.`id_product` = `book`.`id`
	        and `order`.`id_user` = %s
        group by `d_o`.`id_merchandise`
        order by `income` desc
        ;
    ''', [user])

    return income_rank