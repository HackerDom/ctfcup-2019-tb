# Misc | Hidden message

## Информация

> Мы перехватили очередное сообщение от Arbalest of Siberia.
> 
> Этот исполняемый файл ничего не делает.
> 
> Но он явно содержит что-то интересное.
> 
> Может у тебя получится понять, что он скрывает?
> 


## Запуск

Отдать командам файл из deploy/static


## Описание

Бинарный файл, который при загрузке в IDA выдаёт картинку в виде базовых блоков графа.

Суть задания - понять, что бинарь был собран с помощью https://github.com/xoreaxeaxeax/REpsych и декодировать QR-код


## Решение

1. Открыть файл в IDA (это бинарь, можно догодаться)
2. Перейти в режим графов и заметить, что графы сильно напоминают QR-код
3. Меняем цвета графов так, чтобы QR-код стало хорошо видно.
4. Один базовый блок является одним пикселем. Можно перебить руками или как-то иначе.
5. В итоге после чтения QR-кода получим флаг.


## Флаг

`Cup{R3p5ych_R3p5ych_R3p5ych_R3p5ych_1ns4n3}`