from app.database import get_db_connection

# 表头映射字典
COLUMN_MAPPING = {
    'id': '序号',
    'project_name': '项目名称',
    'project_status': '项目状态',
    'industry_chain': '所属产业链',
    'project_content': '项目内容',
    'investor': '投资方',
    'investment_amount': '投资额',
    'financing_amount': '融资额',
    'equity_financing': '股权融资',
    'debt_financing': '债权融资',
    'project_progress': '项目进展及资本对接情况',
    'location': '落地区域',
    'contact_person': '联系人',
    'phone': '电话',
    'contact_phone': '联系方式',
    'fund_name': '基金名称',
    'management_agency': '管理机构',
    'investment_area': '投资领域',
    'fundraising_amount': '募资规模',
    'total_investment': '投资总金额',
    'expert_name': '专家',
    'industry_category': '产业类别',
    'specific_industry': '具体产业',
    'agency_name': '机构名称'
}


# 获取产业ID
def get_industry_id(industry_name):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        "SELECT id FROM KeyIndustries WHERE industry_name = %s", (industry_name, ))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    if result:
        return result['id']
    return None


# 获取产业列表
def get_industries():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT id, industry_name FROM KeyIndustries")
    industries = cursor.fetchall()
    cursor.close()
    connection.close()

    return industries

# Assuming COLUMN_MAPPING and get_db_connection are available here if not passed explicitly


def get_related_data_api(cursor, industry_mapping, current_table_name, industry_id_value):
    """
    获取相关数据 (API Version)
    :param cursor: 数据库游标
    :param industry_mapping: 预先获取的产业ID到名称的映射
    :param current_table_name: 当前查询的主表名 (e.g., 'Expert')
    :param industry_id_value: 要匹配的产业ID值
    :return: 包含相关数据的字典
    """
    # 定义要查询的表及其相应的产业列名 (数据库中的列名)
    # 这些应该是你的数据库中实际存储产业ID的列名
    table_to_industry_column_map = {
        "Expert": "specific_industry",  # 假设这是Expert表中存储产业ID的列
        "Project": "industry_chain",   # 假设这是Project表中存储产业ID的列
        "Fund": "investment_area"      # 假设这是Fund表中存储产业ID的列
    }

    related_data_results = {
        "related_experts": [],
        "related_projects": [],
        "related_funds": []
    }

    if not industry_id_value:  # 如果没有提供产业ID，则不查找相关数据
        return related_data_results

    for table_name_to_query, actual_industry_column_name in table_to_industry_column_map.items():
        if table_name_to_query == current_table_name:
            continue  # 跳过当前正在查询的主表

        # 构建查询语句
        # 重要: 确保 industry_id_value 是正确的类型 (通常是整数) for the query
        query = f"SELECT * FROM {table_name_to_query} WHERE {actual_industry_column_name} = %s"
        try:
            cursor.execute(query, (industry_id_value,))
            results_for_table = cursor.fetchall()
        except Exception as e:
            print(
                f"Error querying related data for {table_name_to_query}: {e}")
            continue  # 如果查询失败，跳到下一个表

        processed_results_for_table = []
        for idx, item_row in enumerate(results_for_table, start=1):
            # 1. 添加序号
            processed_item = {'序号': idx}
            processed_item.update(item_row)  # 合并原始数据

            # 2. 映射产业ID为名称
            if actual_industry_column_name in processed_item:
                processed_item[actual_industry_column_name] = industry_mapping.get(
                    processed_item[actual_industry_column_name], f"未知产业ID: {processed_item[actual_industry_column_name]}"
                )

            # 3. 映射表头 (数据库列名 -> 显示名称)
            final_mapped_item = {
                COLUMN_MAPPING.get(db_col, db_col): val
                for db_col, val in processed_item.items()
            }
            processed_results_for_table.append(final_mapped_item)

        if table_name_to_query == "Expert":
            related_data_results["related_experts"] = processed_results_for_table
        elif table_name_to_query == "Project":
            related_data_results["related_projects"] = processed_results_for_table
        elif table_name_to_query == "Fund":
            related_data_results["related_funds"] = processed_results_for_table

    return related_data_results
