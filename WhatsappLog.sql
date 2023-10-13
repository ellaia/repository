select GSM, count(CNIE) from (
select GSM, CNIE from transactions where to_char(CREATED_AT,'DD/MM/YYYY')='07/10/2023'
and (REGEXP_LIKE(CNIE, '^[A-Za-z]{1,2}\d+$')))
group by GSM order by 2 desc


select count(distinct GSM), count(distinct CNIE) from transactions where to_char(CREATED_AT,'DD/MM/YYYY')='07/10/2023'
and (REGEXP_LIKE(CNIE, '^[A-Za-z]{1,2}\d+$') or CNIE is null)
/*

'جواباً على طلبكم، نعلمكم أن أنه قد تم تحويل المساعدة المالية باسمكم. ويمكنكم التوجه إلى إحدى وكالات القرب المبينة أسفله لسحبها مصحوبين بكود الأداء الدي توصلتم به على هاتفكم.
 _وافاكاش، الفلاحي كاش، كاش بلوس، انوي موني، ضمان كاش، لناكاش، الشعبي كاش، بريد كاش،بريد بنك، تسهيلات، التوفيق_.',
 'نعلمكم أنه لم نتوصل بعد بطلبكم، من الممكن أن يكون قيد المعالجة، وبالتالي، نرجو منكم الانتظار بضعة أيام وإعادة الاتصال بنا',
 'جواباً على طلبكم، نعلمكم أنه قد تم تحويل المساعدة المالية باسمكم وقد تم استخلاصها'
 
 
 */

SELECT MIN(T.CREATED_AT), T.GSM, T.CNIE , DBMS_LOB.SUBSTR(T.RESPONSE, 4000, 1) AS RESPONSE_SUB, DBMS_LOB.SUBSTR(T.MESSAGE, 4000, 1) AS MESSAGE_SUB
FROM TRANSACTIONS T
where  DBMS_LOB.SUBSTR(T.RESPONSE, 4000, 1) like 'جواباً على طلبكم، نعلمكم أنه قد تم تحويل المساعدة المالية باسمكم وقد تم استخلاصها'
and 
to_char(CREATED_AT,'DD/MM/YYYY')='07/10/2023'
group by  T.GSM, T.CNIE, T.GSM, T.CNIE , DBMS_LOB.SUBSTR(T.RESPONSE, 4000, 1) , DBMS_LOB.SUBSTR(T.MESSAGE, 4000, 1)





SELECT count(DISTINCT CNIE) as "Nbr Dossiers", decode(DBMS_LOB.SUBSTR(T.RESPONSE, 4000, 1),'جواباً على طلبكم، نعلمكم أن أنه قد تم تحويل المساعدة المالية باسمكم. ويمكنكم التوجه إلى إحدى وكالات القرب المبينة أسفله لسحبها مصحوبين بكود الأداء الدي توصلتم به على هاتفكم.
 _وافاكاش، الفلاحي كاش، كاش بلوس، انوي موني، ضمان كاش، لناكاش، الشعبي كاش، بريد كاش،بريد بنك، تسهيلات، التوفيق_.','Dossiers consultés pour des mandats émises',
 'نعلمكم أنه لم نتوصل بعد بطلبكم، من الممكن أن يكون قيد المعالجة، وبالتالي، نرجو منكم الانتظار بضعة أيام وإعادة الاتصال بنا','Dossiers consultés non encore traités', 'جواباً على طلبكم، نعلمكم أنه قد تم تحويل المساعدة المالية باسمكم وقد تم استخلاصها','Dossiers consultés pour des mandats payés') as "Libellé"
FROM WHATSAPPLOG.TRANSACTIONS T
WHERE  DBMS_LOB.SUBSTR(T.RESPONSE, 4000, 1) in ('جواباً على طلبكم، نعلمكم أن أنه قد تم تحويل المساعدة المالية باسمكم. ويمكنكم التوجه إلى إحدى وكالات القرب المبينة أسفله لسحبها مصحوبين بكود الأداء الدي توصلتم به على هاتفكم.
 _وافاكاش، الفلاحي كاش، كاش بلوس، انوي موني، ضمان كاش، لناكاش، الشعبي كاش، بريد كاش،بريد بنك، تسهيلات، التوفيق_.',
 'نعلمكم أنه لم نتوصل بعد بطلبكم، من الممكن أن يكون قيد المعالجة، وبالتالي، نرجو منكم الانتظار بضعة أيام وإعادة الاتصال بنا',
 'جواباً على طلبكم، نعلمكم أنه قد تم تحويل المساعدة المالية باسمكم وقد تم استخلاصها'
 )
 AND TO_CHAR(CREATED_AT,'DD/MM/YYYY') in ('06/10/2023','07/10/2023','08/10/2023','09/10/2023','10/10/2023','11/10/2023','12/10/2023','13/10/2023')
 group by DBMS_LOB.SUBSTR(T.RESPONSE, 4000, 1)
 

--group by  T.GSM, T.CNIE


select * from users