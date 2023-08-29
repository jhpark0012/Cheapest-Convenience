import pandas as pd
import pymysql
import warnings

warnings.filterwarnings(action='ignore')

# SQL에서 쿼리문을 통해 테이블을 반환하는 함수
# t: 상품 유형(과자, 음료, 라면), n : 상품 이름, s : 상품 크기 (음료, 라면의 경우)
# return : t, n, s에 해당하는 DataFrame

def get_table_from_mysql(t, n, s):
    # SQL에 연결
    conn = pymysql.connect(host='', user='', password='', db='', charset='')

    ## 상품 가져오기 ##
    if t == "과자":
        SQL = f'''select *
                from  (select *
                from snack_discount natural inner join snack
                where snack_name = "{n}") as T natural inner join discount'''

    elif t == "음료":
        SQL = f'''select *
                from
                    (
                        select *
                        from 
                        (
                        select *
                        from (select *
                        from drink natural inner join drink_capacity
                        where drink_name like "{n}%") as T natural inner join drink_discount
                        )as S natural inner join discount
                    ) as K natural inner join size
                    where size_name = '{s}'
                '''

    elif t == "라면":
        SQL = f'''select *
                from
                (
                select *
                from 
                (
                select *
                from (select *
                from noodle natural inner join noodle_cup_size
                where noodle_name like "{n}%") as T natural inner join noodle_discount
                )as S natural inner join discount
                ) as K natural inner join size
                where size_name = '{s}'
                '''

    # 쿼리문 실행
    res = pd.read_sql_query(SQL, conn)

    conn.close()

    return res


# 최소 금액 리스트를 반환하는 함수
# x: get_table_from_mysql 함수의 반환값, name: 상품 유형, cnt: 상품 개수
# return : 최소 금액 리스트, 상품 유형

def get_min_price_list(x, name, cnt):
    # 최소 금액을 담는 리스트
    price_list = []

    ## 상품 유형 영어로 변환 ##
    if name == '과자':
        name = "snack"

    elif name == "음료":
        name = "drink"

    elif name == "라면":
        name = "noodle"

        ## x를 순회하면서 총 금액 계산 ##
    for idx, row in x.iterrows():
        id_num = int(row["discount_ID"][-1])

        # 단일 상품이면 총금액은 상품 가격 * 상품 개수
        if id_num == 0:
            price = row[f"{name}_price"] * cnt
            price_list.append(price)

        # 할인 상품이면 할인 id를 이용하여 상품 금액 계산
        else:
            price = (cnt // (id_num + 1)) * id_num * row[f"{name}_price"] + (cnt % (id_num + 1) * row[f"{name}_price"])
            price_list.append(price)

    return price_list, name


# 결과를 출력하는 함수
# x : get_min_price_list 함수의 반환값, n: 상품 유형, table: get_table_from_mysql 함수의 반환값

def print_receipt(x, n, table):
    # x가 비어있다면 상품을 잘못 입력한 것
    if not x:
        print('해당 상품은 없습니다.')

    else:
        minimum = min(x)

        # 최솟값을 가지고 있는 인덱스 리스트
        min_idx = [i for i in range(len(x)) if x[i] == minimum]

        # 최종적으로 출력할 데이터 프레임
        end_res = table.loc[min_idx]

        # 과자는 크기가 없으므로 할인 ID 칼럼만 제거
        if n == "snack":
            end_res = end_res.drop(['discount_ID'], axis=1)

        # 라면과 음료는 크기가 있으므로 크기 칼럼도 제거
        else:
            end_res = end_res.drop(['discount_ID', 'size_id', 'size_name'], axis=1)

        end_res["total_price"] = [x[i] for i in min_idx]

        # 할인 남은 기간 : (현재 날짜) - (할인 종료 날짜)
        end_res['left_day'] = pd.Timestamp(2022, 12, 31) - pd.Timestamp(2022, 12, 1)

        # 편의점 이름 순으로 결과를 출력
        end_res = end_res.sort_values(by='store_name')
        print(end_res[["store_name", f"{n}_name", f"{n}_price", "discount_name", "total_price", "left_day"]])


if __name__ == "__main__":
    ## 상품 유형, 상품 이름 입력 ##
    type_order = input("원하는 음식 유형: ")
    name = input(f"원하는 {type_order}의 이름: ")

    # 음료랑 라면만 용량 필요
    if type_order == "음료":
        size = input(f"원하는 {type_order}의 용량: ")

    elif type_order == "라면":
        size = input(f"원하는 {type_order} 사발면 크기: ")

    else:
        size = None

    ## 상품 개수 입력 ##
    count = int(input(f'{name}의 개수를 입력: '))

    print('###################################################################################')

    res = get_table_from_mysql(type_order, name, size)  # SQL문으로 받은 TABLE

    min_price_list, name_eng = get_min_price_list(res, type_order, count)  # 최소 금액 LIST, 상품 영어 이름

    print_receipt(min_price_list, name_eng, res)  # 결과 출력