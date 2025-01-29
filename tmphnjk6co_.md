## Assignment 03 - Basic SQL

Using the EMP and DEPT table (where ever applicable) that were created as part of workshop session Answer the following questions.

oracle-scott-schema-tables.sql

sqlServer-scott-schema-tables.sql

## Questions

## Oracle SQL

- List name and salary of employees whose salary is more than 1000

SELECT ENAME, SAL FROM EMP

WHERE SAL > 1000;

![Image](tmphnjk6co__artifacts/image_000000_14e8639765cfcd90772eadfed24731a6c0e9968efcceae2529d5ee8ad3cf6f26.png)

- List names of CLERK's working in department 20

SELECT ENAME FROM EMP WHERE JOB='CLERK' and DEPTNO=20;

![Image](tmphnjk6co__artifacts/image_000001_57d474402574e8c773eae64d7c06fa5b2fd85e92c325c5b647e483f1b309b7c8.png)

- List employee names of job type analysts, salesmen

SELECT ENAME FROM EMP

WHERE JOB IN ('ANALYST', 'SALESMAN');

![Image](tmphnjk6co__artifacts/image_000002_9e37df31af3446c6df05e1d1aac992d3e4fae504762bcd37d0a6517f076f9835.png)

- List names of employees who are not managers

SELECT EMPNO, ENAME FROM EMP WHERE EMPNO NOT IN ( SELECT MGR FROM EMP WHERE MGR IS NOT NULL);

![Image](tmphnjk6co__artifacts/image_000003_b398a6bf2257c2cd8231e6c43c1fe39b3e786abe310374e22db04011e6f22d42.png)

- List name of employees whose employee numbers are 7369, 7521, 7934, 7788

SELECT ENAME FROM EMP

```
WHERE EMPNO IN (7369, 7521, 7934, 7788);
```

![Image](tmphnjk6co__artifacts/image_000004_6831559b0424cb1376da808e0197513e5925efff971e421c57d828360dc2e2bf.png)

- List employee names who doesn't belong to department 20, 30

SELECT ENAME FROM EMP

WHERE DEPTNO NOT IN (20, 30);

![Image](tmphnjk6co__artifacts/image_000005_5807d4e5443f39359457dbca55ba68c9d499eb242bea91171821bf70f7ec219e.png)

- List employee name and salary whose salary is between 1000 and 2000

SELECT ENAME FROM EMP WHERE SAL BETWEEN 1000 AND 2000;

![Image](tmphnjk6co__artifacts/image_000006_549ea90b013fe7b11d8cce15c0bca22dabfb5f29494cead616c4d6b1010e4967.png)

- List different jobs available in EMP table

SELECT DISTINCT JOB FROM EMP;

![Image](tmphnjk6co__artifacts/image_000007_6b73273a2ce940bb377707a8d4af23ca81c401c6ba308521574454d52c1dcace.png)

## List department names and locations from DEPT table

SELECT DNAME, LOC FROM DEPT;

![Image](tmphnjk6co__artifacts/image_000008_5497e7a24d3d5d55b5d3be3f9425535d1b296c43603e2746c04e989b56544960.png)

- List employee names who have joined during the period of 30th June 1981 and 31st December 1981

SELECT ENAME FROM EMP WHERE HIREDATE BETWEEN '30-JUN-81' AND '31-DEC-81';

![Image](tmphnjk6co__artifacts/image_000009_14f3ae679e52bb485326145ff66fa44dff8cb3fbc6d93495d40a688da85de8b7.png)

- List employees whose names start with capital "S"

```
SELECT ENAME FROM EMP WHERE ENAME LIKE 'S%';
```

![Image](tmphnjk6co__artifacts/image_000010_4057a7b3944f3e0691a8d863c2b4ffe6e6b8f873219a66835afce54081696fbd.png)

- List names of employee having "I" as second character

SELECT ENAME FROM EMP WHERE ENAME LIKE '\_I%';

![Image](tmphnjk6co__artifacts/image_000011_f2ea33938728e3dc51fa4c38e4080101d4133d6a67cdbf1fd21e971be24e7869.png)

- List name, sal and Calculate 10% bonus amount based on their salary for each employee

SELECT ENAME, SAL, SAL * 0.1 as BONUS FROM EMP;

![Image](tmphnjk6co__artifacts/image_000012_b5de3f66e6e2292cf45de5c561e7ca6b74d887f306c33e102a6a7516b695d4f9.png)

- Using catalog tables, generate an output which displays tablename, column name, datatype and its width of all the tables that are available under the user that you logged in. Expected to see the details of tables EMP, DEPT and SALGRADE

SELECT TABLE\_NAME, COLUMN\_NAME, DATA\_TYPE, DATA\_LENGTH FROM USER\_TAB\_COLUMNS;

![Image](tmphnjk6co__artifacts/image_000013_6b2fdbb3fdb855441e1a0fdce5bf4b6ea9c08f6f8e46b9d0d2f46962bb34012f.png)

- List details from table emp where ename ends with 'H' and contains 5 characters.

SELECT * FROM EMP

WHERE ENAME LIKE '\_\_\_\_H';

![Image](tmphnjk6co__artifacts/image_000014_cc6c2cf79062d2cca385e06bafdae53845817557a38d8579f60bef3713a18074.png)

- List details of the employee's who joined on 3rd December, 1981.

SELECT * FROM EMP

WHERE HIREDATE='03-DEC-81';

![Image](tmphnjk6co__artifacts/image_000015_7ef49e4265b9894ec874e64f4209f62f823fcebe89c8718e4658678bed9a7115.png)

- Write an SQL statement to print current database server date and time along with logged in username Hint: use USER for oracle and CURRENT\_USER for SQL Server / sysdate for oracle and getdate() for SQL Server)

SELECT USER,

```
TO\_CHAR(SYSDATE, 'DD-MON-YYYY HH24:MI:SS') AS CURRENT\_DATE FROM DUAL;
```

![Image](tmphnjk6co__artifacts/image_000016_09abe600d18abad7acec996fcd2ac0dc8b7dcc8490509f89477e602bd42130eb.png)

- List all employee names which has a character '\_' Underscore)

SELECT ENAME FROM EMP WHERE ENAME LIKE '%\_%' ESCAPE '\';

![Image](tmphnjk6co__artifacts/image_000017_edb0218ce569320cc79a075003dc65aae6cf6b917720f434f2e668f56248dbdd.png)

- List employee names who belongs to department 20 and 30 with salary greater than 1500

SELECT ENAME FROM EMP

WHERE DEPTNO IN (20,30) AND SAL > 1500;

![Image](tmphnjk6co__artifacts/image_000018_a8b03b11e4ab28b83c1dedd345b17adbbf918b82f55c88c4bb5432f944df980d.png)

- List all department names and locations. Available in table DEPT

SELECT DNAME, LOC FROM DEPT;

![Image](tmphnjk6co__artifacts/image_000019_8a4d5ec7a6c6b94cdb20bc8045730a80ccfd1b88bff63d574577824110a28cd6.png)