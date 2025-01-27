### Difference Between Interlock `IL` `ILC` and Jump `JMP` `JME`

| Condition           | Interlock `IL` `ILC`                                                 | Jump `JMP` `JME`                                                              |
| ------------------- | -------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| if `IL` `JMP` is `1` | output ตาม condition ของ Ladder Diagram ที่อยู่ในช่วง `IL` ถึง `ILC` | output ตาม Ladder Diagram ที่อยู่ในช่วง `JMP` ถึง `JME`                       |
| if `IL` `JMP` is `0` | output ทุกตัวที่อยู่ในช่วง `IL` ถึง `ILC` จะเป็น `0` ทั้งหมด         | output ทุกตัวที่อยู่ในช่วง `JMP` ถึง `JME` จะคงค่าเดิม (ตอนก่อนที่จะเป็น `0`) |

### Difference Between Set `SET`, Reset `RSET` and Keep `KEEP`

Set `SET` - ตั้งค่าให้เป็นใน bit นั้น `1`

Reset `RSET` - ตั้งค่าให้เป็นใน bit นั้น `0`

Keep `KEEP` - เหมือน set + reset ในอันเดียว

### Difference Between Differentiate Up `DIFU` and Differentiate Down `DIFD`

Differentiate Up `DIFU` - Output `1` เป็นเวลาเพียง 1 Cycle ในช่วงที่สัญญาณที่กำลังขึ้น

Differentiate Down `DIFD` - Output `1` เป็นเวลาเพียง 1 Cycle ในช่วงที่สัญญาณที่กำลังลง
