
::
  curl -H 'Content-Type: application/json; charset=UTF-8' -X POST --data @test.json  http://192.168.0.5:8222/api/event/

  [tvdv@kvm ~]$ cat test.json
      {
          "type": 1,
          "desc": "Machine for test, please do not delete!"
      }
      [tvdv@kvm ~]$
