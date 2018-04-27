from random import random
from scipy import stats
import re
import math

test_sum = 0.0 
index_sum = 0.0
home_sum = 0.0

test_count = 0
index_count = 0
home_count = 0

time_regex = re.compile('\d+.\d+')  

with open('log.txt', 'r') as log:
    for line in log:
        
        if 'test' in line:
            try:
                times = time_regex.search(line).group(0)
            except (TypeError, AttributeError):
                times = 0
            test_sum += float(times)
            test_count += 1
            
        if 'index' in line:
            try:
                times = time_regex.search(line).group(0)
            except (TypeError, AttributeError):
                times = 0
            index_sum += float(times)
            index_count += 1
            
        if 'home' in line:
            try:
                times = time_regex.search(line).group(0)
            except (TypeError, AttributeError):
                times = 0
            home_sum += float(times)
            home_count += 1

test_mean = test_sum/test_count
index_mean = index_sum/index_count
home_mean = home_sum/home_count

print "Среднее время для /test:", test_mean, ", Число запросов /test", test_count
print "Среднее время для /index:", index_mean, ", Число запросов /index", index_count
print "Среднее время /home:", home_mean, ", Число запросов /home", home_count

test_tmp = 0.0
index_tmp = 0.0
home_tmp = 0.0

with open('log.txt', 'r') as log:
    for line in log:
        
        if 'test' in line:
            try:
                times = time_regex.search(line).group(0)
            except (TypeError, AttributeError):
                times = 0
            test_tmp += (float(times) - test_mean)**2
        
        if 'index' in line:
            try:
                times = time_regex.search(line).group(0)
            except (TypeError, AttributeError):
                times = 0
            index_tmp += (float(times) - index_mean)**2
        
        if 'home' in line:
            try:
                times = time_regex.search(line).group(0)
            except (TypeError, AttributeError):
                times = 0
            home_tmp += (float(times)- home_mean)**2

test_std = math.sqrt((1.0/test_count) * test_tmp)
index_std = math.sqrt((1.0/index_count) * index_tmp)
home_std = math.sqrt((1.0/home_count) * home_tmp)

print "Стандартное отклонение для /test", test_std
print "Стандартное отклонение для /index", index_std
print "Стандартное отклонение для /index", home_std

test_sem = test_std / math.sqrt(test_count)
index_sem = index_std / math.sqrt(index_count)
home_sem = home_std / math.sqrt(home_count)

print "Стандартная ошибка для /test", test_sem
print "Стандартная ошибка для /index", index_sem
print "Стандартная ошибка для /home", home_sem

conf_test_mean = stats.t.interval(0.95, test_count, test_mean, test_sem)
print "Доверительный интервал среднего для /test (если считать исходное распределение за Стьюдента)", conf_test_mean
conf_index_mean = stats.t.interval(0.95, index_count, index_mean, index_sem)
print "Доверительный интервал среднего для /index (если считать исходное распределение за Стьюдента)", conf_index_mean
conf_home_mean = stats.t.interval(0.95, home_count, home_mean, home_sem)
print "Доверительный интервал среднего для /home (если считать исходное распределение за Стьюдента)", conf_home_mean

print "\n"

conf_test_mean = stats.norm.interval(0.95, test_mean, test_sem)
print "Доверительный интервал среднего для /test (если считать исходное распределение за нормальное)", conf_test_mean
conf_index_mean = stats.norm.interval(0.95, index_mean, index_sem)
print "Доверительный интервал среднего для /index (если считать исходное распределение за нормальное)", conf_index_mean
conf_home_mean = stats.norm.interval(0.95,  home_mean, home_sem)
print "Доверительный интервал среднего для /home (если считать исходное распределение за нормальное)", conf_home_mean

t_test_des = stats.ttest_ind_from_stats(test_mean, test_std, test_count, index_mean, index_std, index_count, equal_var=False)
if t_test_des.pvalue > 0.05:
    print "t-тест для дескриптивных статистик: Средние значения равны на уровне 5%, p-value =", t_test_des.pvalue, "Cтатистика теста", t_test_des.statistic
else:
    print "t-тест для дескриптивных статистик: Средние значения не равны, p-value =", t_test_des.pvalue, "Cтатистика теста", t_test_des.statistic