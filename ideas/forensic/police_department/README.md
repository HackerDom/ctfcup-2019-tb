# Forensic | Police Department

## Информация

> Нам написал наш агент, Ливи из полицеского департамента, в письме была просьба узнать код безопасности корпорации Arbalests of Siberia, также в письме был указан не то ключ, не то шифр, и приложен странный файл, кажется это запись работы древней технологии, надеюсь, ты разберешься. Удачи.
>
> 'ce95c9510a104a05954c244afb3fee182f9b813086d95889abc8e92cc6253bbd'
>
> Ответ: Cup{md5(security_code)}

## Описание

Дан [дамп](https://drive.google.com/open?id=1z5_AiNwqbz1OPDkPVw8tpA5hezvFHtZk)  сети и ключ



## Решение

Если поизучать трафик, то можно заметить наличие протокола EAP, в котором происходит WPS аутентификация. В дампе всего три сообщения M1, M2, M3, что дает возможность провесити атаку Pixie Dust, основанную на уязвимости генератора рандома в прошивках некоторых вендоров. Для проведения данной атаки по дампу трафика необходимо найти следующие параметры: 

* Enrollee public key (PKE) в сообщении M1
* Enrollee nonce (e-nonce) в сообщении M1
* Registrar public key (PKR) в сообщении M2
* Enrollee hash-1 (e-hash1) в сообщении M3
* Enrollee hash-2 (e-hash2) в сообщении M3

Однако найти `Authentication session key (authkey)` в сообщениях протокола EAP невозможно, поэтому воспользуемся ключем приложенным к заданию, в качестве `authkey`. Получив все необходимые параметры, воспользуемся утилитой `pixiewps` для нахождения WPS pin. 

```bash
 $ pixiewps -e PKE -s e-hash1 -z e-hash2 -a authkey -n e-nonce -r PKR
 Pixiewps 1.4

 [?] Mode:     1 (RT/MT/CL)
 [*] Seed N1:  0xab60aaf8
 [*] Seed ES1: 0x278bf66e
 [*] Seed ES2: 0x28545033
 [*] PSK1:     8ac1371f35529b32ffedfdf1e9a09573
 [*] PSK2:     332f170151f83e5cb781432525be5f80
 [*] ES1:      42be658ec0b914d1a7590cd0ebf9e60c
 [*] ES2:      b112b9e6e81ea3a4837a3fe69eccfdb3
 [+] WPS pin:  63969641

 [*] Time taken: 0 s 722 ms
```

Далее возьмем md5('63969641') => fb6a6ef793ef41bb4d957891ef6e7dfb



## Флаг

Cup{fb6a6ef793ef41bb4d957891ef6e7dfb}