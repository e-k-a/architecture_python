# ДЗ 5

1.Для данных, хранящихся в реляционной базе PotgreSQL реализуйте шаблон сквозное чтение и сквозная запись (Пользователь/Клиент …);
2.В качестве кеша –используйте Redis
3.Замерьте производительность запросов на чтение данных с и без кеша с использованием утилиты wrk https://github.com/wg/wrk изменяя количество потоков из которых производятся запросы (1, 5, 10)
4.Актуализируйте модель архитектуры в Structurizr DSL
5.Ваши сервисы должны запускаться через docker-compose командой docker-compose up(создайте Dockerфайлы для каждого сервиса)



```
docker-compose exec wrk wrk -t10 -c10 -d10s http://auth:8000/me -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI1MSIsImV4cCI6MTc0NjU2NDQ2OH0.LOBMecEIkE3XVx_E8tlnuExBGk5CCZpS0-3JY_jigfQ"
Running 10s test @ http://auth:8000/me
  10 threads and 10 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    24.06ms    6.11ms  73.86ms   91.31%
    Req/Sec    41.83      7.72    90.00     52.50%
  4187 requests in 10.05s, 658.43KB read
Requests/sec:    416.70
Transfer/sec:     65.53KB
```

```
docker-compose exec wrk wrk -t5 -c10 -d10s http://auth:8000/me -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI1MSIsImV4cCI6MTc0NjU2NDQ2OH0.LOBMecEIkE3XVx_E8tlnuExBGk5CCZpS0-3JY_jigfQ"
Running 10s test @ http://auth:8000/me
  5 threads and 10 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    31.82ms   43.36ms 411.51ms   96.81%
    Req/Sec    81.13     14.54   101.00     75.73%
  3938 requests in 10.03s, 619.16KB read
Requests/sec:    392.43
Transfer/sec:     61.70KB
```

```
docker-compose exec wrk wrk -t1 -c10 -d10s http://auth:8000/me -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI1MSIsImV4cCI6MTc0NjU2NDQ2OH0.LOBMecEIkE3XVx_E8tlnuExBGk5CCZpS0-3JY_jigfQ"
Running 10s test @ http://auth:8000/me
  1 threads and 10 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    27.07ms    8.17ms 103.92ms   89.20%
    Req/Sec   373.98     70.30   474.00     75.00%
  3726 requests in 10.01s, 585.95KB read
Requests/sec:    372.11
Transfer/sec:     58.52KB
```