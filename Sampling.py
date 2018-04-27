import random
from scipy import stats
import re
import math

time_regex = re.compile('\d+.\d+')

trials = 10000
sample_size = 2000
i = 0
test_sample = []
index_sample = []
home_sample = []
random_set = []

with open('log.txt', 'rb') as log:
    
    log.seek(0, 2)
    log_size = log.tell()
    # Определяем размер файла
    
    for trial in xrange(trials):
        random_set.append(random.choice(xrange(log_size)))
    # Делаем выборку позиций байтов.
    
    while (len(test_sample) < sample_size) | (len(index_sample) < sample_size) | (len(home_sample) < sample_size):
        
        log.seek(random_set[i]) # Выбираем следующую позицию байтов из выборки
        log.readline() # Пропускаем линию, на случай, если попали в середину строки
        line = log.readline().rstrip()
    
        if ('test' in line) & (len(test_sample) < sample_size):
            try:
                times = time_regex.search(line).group(0)
            except (TypeError, AttributeError):
                times = 0
            test_sample.append(float(times))
        
        if ('index' in line) & (len(index_sample) < sample_size):
            try:
                times = time_regex.search(line).group(0)
            except (TypeError, AttributeError):
                times = 0
            index_sample.append(float(times))
        
        if ('home' in line) & (len(home_sample) < sample_size):
            try:
                times = time_regex.search(line).group(0)
            except (TypeError, AttributeError):
                times = 0
            home_sample.append(float(times))
        # Собираем выборку для каждого запроса. Регэкс может вернуть None, поэтому обернут в try-except.
        
        if i < (len(random_set)-1):
            i += 1
        else:
            for trial in xrange(trials):
                random_set.append(random.choice(xrange(log_size)))
            i = 0
        # Если по выборке байтов прошли, но нужные выборки не набрались, имеет смысл сделать новую выборку байтов.

home_mean = stats.describe(home_sample).mean
home_variance = stats.describe(home_sample).variance
home_nobs= stats.describe(home_sample).nobs
home_std = math.sqrt(home_variance)

print "Среднее значение для /home", home_mean

index_mean = stats.describe(index_sample).mean
index_variance = stats.describe(index_sample).variance
index_nobs= stats.describe(index_sample).nobs
index_std = math.sqrt(index_variance)

print "Среднее значение для /index", index_mean

test_mean = stats.describe(test_sample).mean
test_variance = stats.describe(test_sample).variance
test_nobs= stats.describe(test_sample).nobs
test_std = math.sqrt(test_variance)

print "Среднее значение для /test", test_mean

conf_test_mean = stats.t.interval(0.95, len(test_sample), test_mean, stats.sem(test_sample))
print "Доверительный интервал среднего для /test (если считать исходное распределение за Стьюдента)", conf_test_mean
conf_home_mean = stats.t.interval(0.95, len(home_sample), home_mean, stats.sem(home_sample))
print "Доверительный интервал среднего для /home (если считать исходное распределение за Стьюдента)", conf_home_mean
conf_index_mean = stats.t.interval(0.95, len(index_sample), index_mean, stats.sem(index_sample))
print "Доверительный интервал среднего для /index (если считать исходное распределение за Стьюдента)", conf_index_mean

print "\n"

conf_test_mean = stats.norm.interval(0.95, test_mean, stats.sem(test_sample))
print "Доверительный интервал среднего для /test (если считать исходное распределение за нормальное)", conf_test_mean
conf_home_mean = stats.norm.interval(0.95,  home_mean, stats.sem(home_sample))
print "Доверительный интервал среднего для /home (если считать исходное распределение за нормальное)", conf_home_mean
conf_index_mean = stats.norm.interval(0.95, index_mean, stats.sem(index_sample))
print "Доверительный интервал среднего для /index (если считать исходное распределение за нормальное)", conf_index_mean

t_test = stats.ttest_ind(test_sample, index_sample)
if t_test.pvalue > 0.05:
    print "t-тест: Средние значения равны на уровне 5%, p-value =", t_test.pvalue, "Cтатистика теста", t_test.statistic
else:
    print "t-тест: Средние значения не равны, p-value =", t_test.pvalue, "Cтатистика теста", t_test.statistic

t_test_des = stats.ttest_ind_from_stats(test_mean, test_std, test_nobs, index_mean, index_std, index_nobs, equal_var=False)
if t_test_des.pvalue > 0.05:
    print "t-тест для дескриптивных статистик: Средние значения равны на уровне 5%, p-value =", t_test_des.pvalue, "Cтатистика теста", t_test_des.statistic
else:
    print "t-тест для дескриптивных статистик: Средние значения не равны, p-value =", t_test_des.pvalue, "Cтатистика теста", t_test_des.statistic

kstest = stats.ks_2samp(test_sample, index_sample)
if kstest.pvalue > 0.05:
    print "Тест Колмогорова-Смирнова: Распределения выборок равны на уровне 5%, p-value =", kstest.pvalue, "Cтатистика теста", kstest.statistic
else:
    print "Тест Колмогорова-Смирнова: Распределения выборок не равны, p-value =", kstest.pvalue, "Cтатистика теста", kstest.statistic

mwtest = stats.mannwhitneyu(test_sample, index_sample)
if mwtest.pvalue > 0.05:
    print "Тест Манн-Уитни: Распределения выборок равны на уровне 5%, p-value =", mwtest.pvalue, "Cтатистика теста", mwtest.statistic
else:
    print "Тест Манн-Уитни: Распределения выборок не равны, p-value =", mwtest.pvalue, "Cтатистика теста", mwtest.statistic