/* Formatted on 12/10/2023 20:16:44 (QP5 v5.326) */
CREATE TABLE WHAT_DAAM
AS
    (SELECT DISTINCT T.GSM AS NUM_WHATSAPP, UPPER(T.CNIE) AS CNIE
       FROM WHATSAPPLOG.TRANSACTIONS T
      WHERE     DBMS_LOB.SUBSTR (T.RESPONSE, 4000, 1) LIKE
                    '?????? ??? ?????? ?????? ?? ??? ?? ?? ????? ???????? ??????? ??????. ??????? ?????? ??? ???? ?????? ????? ??????? ????? ?????? ??????? ???? ?????? ???? ?????? ?? ??? ??????.
 _???????? ??????? ???? ??? ????? ???? ????? ???? ???? ??????? ?????? ???? ???? ???????? ???? ???????? ???????_.'
            AND (REGEXP_LIKE (CNIE, '^[A-Za-z]{1,2}\d+$'))
            AND T.CNIE IN (SELECT UPPER(mad.cnie)
                             FROM pp_pay_mad mad
                            WHERE CURRENT_STATUT = 'GENERE')
)

create table DAAM_WHA as 
select DISTINCT mad.GSM1, UPPER(mad.cnie) as CNIE from pp_pay_mad mad where CURRENT_STATUT = 'GENERE'
and UPPER(mad.cnie) in (SELECT DISTINCT UPPER(T.CNIE)
FROM WHATSAPPLOG.TRANSACTIONS T
where  DBMS_LOB.SUBSTR(T.RESPONSE, 4000, 1) like '?????? ??? ?????? ?????? ?? ??? ?? ?? ????? ???????? ??????? ??????. ??????? ?????? ??? ???? ?????? ????? ??????? ????? ?????? ??????? ???? ?????? ???? ?????? ?? ??? ??????.
 _???????? ??????? ???? ??? ????? ???? ????? ???? ???? ??????? ?????? ???? ???? ???????? ???? ???????? ???????_.'
and (REGEXP_LIKE(CNIE, '^[A-Za-z]{1,2}\d+$'))
)
order by 2 desc

select count(*) from WHAT_DAAM

select DW.GSM1 as GSM_MI, WD.NUM_WHATSAPP as GSM_WHATSAPP, DW.CNIE from DAAM_WHA DW, WHAT_DAAM WD
where wd.cnie = dw.cnie

select * from WHAT_DAAM


select * from pp_pay_mad

SELECT distinct mad.current_statut 
--DISTINCT mad.*,
--d.LIBF_QUARTIER_DOUAR,
--d.LIBF_COMMUNE,
--d.LIBF_PROVINCE
FROM pp_pay_mad mad --, DETAIL_FICHIER_ALLER mi, douar_mi d
--WHERE     mad.cnie = mi.cin
--       AND mi.CODE_DOUAR_MI = d.ID_QUARTIER_DOUAR
--       AND mi.CODE_COMMUNE_MI = d.ID_COMMUNE
      -- AND d.LIBF_PROVINCE ='HAOUZ'
      -- AND d.LIBF_COMMUNE ='AMIZMIZ'
       --AND d.LIBF_QUARTIER_DOUAR = "AGOUN"
    
  

  
    SELECT DISTINCT mad.CNIE, mad.current_statut, d.LIBA_QUARTIER_DOUAR, d.LIBA_COMMUNE, d.LIBA_PROVINCE
  FROM pp_pay_mad mad, DETAIL_FICHIER_ALLER mi, douar_mi d
 WHERE     mad.cnie = mi.cin
       AND mi.CODE_DOUAR_MI = d.ID_QUARTIER_DOUAR
       AND mi.CODE_COMMUNE_MI = d.ID_COMMUNE
    ----   AND mad.CURRENT_STATUT='PAYE'
    
    
 SELECT d.LIBA_PROVINCE, d.LIBA_COMMUNE, d.LIBA_QUARTIER_DOUAR, decode(mad.current_statut,'GENERE','?? ??? ???????? ???? ????? ???','PAYE','??? ???????? ???? ?????','VEROUILLE','?? ??? ??????? ???? ???????? ???? ?????') as "Etat", count(*)
  FROM pp_pay_mad mad, DETAIL_FICHIER_ALLER mi, douar_mi d
 WHERE     mad.cnie = mi.cin
       AND mi.CODE_DOUAR_MI = d.ID_QUARTIER_DOUAR
       AND mi.CODE_COMMUNE_MI = d.ID_COMMUNE
       group by mad.current_statut, d.LIBA_QUARTIER_DOUAR, d.LIBA_COMMUNE, d.LIBA_PROVINCE
       order by 1,2,3
    ----   AND mad.CURRENT_STATUT='PAYE'
    
    
    
     
 SELECT d.LIBF_PROVINCE, d.LIBF_COMMUNE , --d.LIBF_QUARTIER_DOUAR,
 decode(mad.current_statut,'GENERE','NON ENCORE RETIRE','PAYE','RETIRE','VEROUILLE','EN COURS') as "Etat", count(*)
  FROM pp_pay_mad mad, DETAIL_FICHIER_ALLER mi, douar_mi d
 WHERE     mad.cnie = mi.cin
       AND mi.CODE_DOUAR_MI = d.ID_QUARTIER_DOUAR
       AND mi.CODE_COMMUNE_MI = d.ID_COMMUNE
       group by mad.current_statut, d.LIBF_PROVINCE, d.LIBF_COMMUNE--, d.LIBF_QUARTIER_DOUAR
       order by 1,2,3
    ----   AND mad.CURRENT_STATUT='PAYE'
    
    
    
SELECT d.LIBF_PROVINCE as "Province", d.LIBF_COMMUNE as "Commune", decode(mad.current_statut,'GENERE','NON ENCORE RETIRE','PAYE','RETIRE','VEROUILLE','EN COURS') as "Etat", count(*) as "Nombre"
  FROM pp_pay_mad mad, DETAIL_FICHIER_ALLER mi, douar_mi d
 WHERE     mad.cnie = mi.cin
       AND mi.CODE_DOUAR_MI = d.ID_QUARTIER_DOUAR
       AND mi.CODE_COMMUNE_MI = d.ID_COMMUNE
       group by mad.current_statut, d.LIBF_PROVINCE, d.LIBF_COMMUNE
       order by 1,2,3
       
       select * from pp_pay_mad
       
       SELECT mad.*, d.LIBF_PROVINCE as "PROVINCE"
  FROM pp_pay_mad mad, DETAIL_FICHIER_ALLER mi, douar_mi d
 WHERE     mad.cnie = mi.cin
       AND mi.CODE_DOUAR_MI = d.ID_QUARTIER_DOUAR
       AND mi.CODE_COMMUNE_MI = d.ID_COMMUNE
       --group by mad.current_statut, d.LIBF_PROVINCE, d.LIBF_COMMUNE--, d.LIBF_QUARTIER_DOUAR
 
    
    