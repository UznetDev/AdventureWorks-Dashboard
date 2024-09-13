# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Adventureworksdwbuildversion(models.Model):
    dbversion = models.CharField(db_column='DBVersion', max_length=50, blank=True, null=True)  # Field name made lowercase.
    versiondate = models.DateTimeField(db_column='VersionDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'AdventureWorksDWBuildVersion'


class Databaselog(models.Model):
    databaselogid = models.AutoField(db_column='DatabaseLogID', primary_key=True)  # Field name made lowercase.
    posttime = models.DateTimeField(db_column='PostTime')  # Field name made lowercase.
    databaseuser = models.CharField(db_column='DatabaseUser', max_length=128)  # Field name made lowercase.
    event = models.CharField(db_column='Event', max_length=128)  # Field name made lowercase.
    schema = models.CharField(db_column='Schema', max_length=128, blank=True, null=True)  # Field name made lowercase.
    object = models.CharField(db_column='Object', max_length=128, blank=True, null=True)  # Field name made lowercase.
    tsql = models.TextField(db_column='TSQL')  # Field name made lowercase.
    xmlevent = models.TextField(db_column='XmlEvent')  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'DatabaseLog'


class Dimaccount(models.Model):
    accountkey = models.AutoField(db_column='AccountKey', primary_key=True)  # Field name made lowercase.
    parentaccountkey = models.ForeignKey('self', models.DO_NOTHING, db_column='ParentAccountKey', blank=True, null=True)  # Field name made lowercase.
    accountcodealternatekey = models.IntegerField(db_column='AccountCodeAlternateKey', blank=True, null=True)  # Field name made lowercase.
    parentaccountcodealternatekey = models.IntegerField(db_column='ParentAccountCodeAlternateKey', blank=True, null=True)  # Field name made lowercase.
    accountdescription = models.CharField(db_column='AccountDescription', max_length=50, blank=True, null=True)  # Field name made lowercase.
    accounttype = models.CharField(db_column='AccountType', max_length=50, blank=True, null=True)  # Field name made lowercase.
    operator = models.CharField(db_column='Operator', max_length=50, blank=True, null=True)  # Field name made lowercase.
    custommembers = models.CharField(db_column='CustomMembers', max_length=300, blank=True, null=True)  # Field name made lowercase.
    valuetype = models.CharField(db_column='ValueType', max_length=50, blank=True, null=True)  # Field name made lowercase.
    custommemberoptions = models.CharField(db_column='CustomMemberOptions', max_length=200, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DimAccount'


class Dimcurrency(models.Model):
    currencykey = models.AutoField(db_column='CurrencyKey', primary_key=True)  # Field name made lowercase.
    currencyalternatekey = models.CharField(db_column='CurrencyAlternateKey', unique=True, max_length=3)  # Field name made lowercase.
    currencyname = models.CharField(db_column='CurrencyName', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DimCurrency'


class Dimcustomer(models.Model):
    customerkey = models.AutoField(db_column='CustomerKey', primary_key=True)  # Field name made lowercase.
    geographykey = models.ForeignKey('Dimgeography', models.DO_NOTHING, db_column='GeographyKey', blank=True, null=True)  # Field name made lowercase.
    customeralternatekey = models.CharField(db_column='CustomerAlternateKey', unique=True, max_length=15)  # Field name made lowercase.
    title = models.CharField(db_column='Title', max_length=8, blank=True, null=True)  # Field name made lowercase.
    firstname = models.CharField(db_column='FirstName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    middlename = models.CharField(db_column='MiddleName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    lastname = models.CharField(db_column='LastName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    namestyle = models.NullBooleanField(db_column='NameStyle')  # Field name made lowercase.
    birthdate = models.DateField(db_column='BirthDate', blank=True, null=True)  # Field name made lowercase.
    maritalstatus = models.CharField(db_column='MaritalStatus', max_length=1, blank=True, null=True)  # Field name made lowercase.
    suffix = models.CharField(db_column='Suffix', max_length=10, blank=True, null=True)  # Field name made lowercase.
    gender = models.CharField(db_column='Gender', max_length=1, blank=True, null=True)  # Field name made lowercase.
    emailaddress = models.CharField(db_column='EmailAddress', max_length=50, blank=True, null=True)  # Field name made lowercase.
    yearlyincome = models.DecimalField(db_column='YearlyIncome', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    totalchildren = models.SmallIntegerField(db_column='TotalChildren', blank=True, null=True)  # Field name made lowercase.
    numberchildrenathome = models.SmallIntegerField(db_column='NumberChildrenAtHome', blank=True, null=True)  # Field name made lowercase.
    englisheducation = models.CharField(db_column='EnglishEducation', max_length=40, blank=True, null=True)  # Field name made lowercase.
    spanisheducation = models.CharField(db_column='SpanishEducation', max_length=40, blank=True, null=True)  # Field name made lowercase.
    frencheducation = models.CharField(db_column='FrenchEducation', max_length=40, blank=True, null=True)  # Field name made lowercase.
    englishoccupation = models.CharField(db_column='EnglishOccupation', max_length=100, blank=True, null=True)  # Field name made lowercase.
    spanishoccupation = models.CharField(db_column='SpanishOccupation', max_length=100, blank=True, null=True)  # Field name made lowercase.
    frenchoccupation = models.CharField(db_column='FrenchOccupation', max_length=100, blank=True, null=True)  # Field name made lowercase.
    houseownerflag = models.CharField(db_column='HouseOwnerFlag', max_length=1, blank=True, null=True)  # Field name made lowercase.
    numbercarsowned = models.SmallIntegerField(db_column='NumberCarsOwned', blank=True, null=True)  # Field name made lowercase.
    addressline1 = models.CharField(db_column='AddressLine1', max_length=120, blank=True, null=True)  # Field name made lowercase.
    addressline2 = models.CharField(db_column='AddressLine2', max_length=120, blank=True, null=True)  # Field name made lowercase.
    phone = models.CharField(db_column='Phone', max_length=20, blank=True, null=True)  # Field name made lowercase.
    datefirstpurchase = models.DateField(db_column='DateFirstPurchase', blank=True, null=True)  # Field name made lowercase.
    commutedistance = models.CharField(db_column='CommuteDistance', max_length=15, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DimCustomer'


class Dimdate(models.Model):
    datekey = models.IntegerField(db_column='DateKey', primary_key=True)  # Field name made lowercase.
    fulldatealternatekey = models.DateField(db_column='FullDateAlternateKey', unique=True)  # Field name made lowercase.
    daynumberofweek = models.SmallIntegerField(db_column='DayNumberOfWeek')  # Field name made lowercase.
    englishdaynameofweek = models.CharField(db_column='EnglishDayNameOfWeek', max_length=10)  # Field name made lowercase.
    spanishdaynameofweek = models.CharField(db_column='SpanishDayNameOfWeek', max_length=10)  # Field name made lowercase.
    frenchdaynameofweek = models.CharField(db_column='FrenchDayNameOfWeek', max_length=10)  # Field name made lowercase.
    daynumberofmonth = models.SmallIntegerField(db_column='DayNumberOfMonth')  # Field name made lowercase.
    daynumberofyear = models.SmallIntegerField(db_column='DayNumberOfYear')  # Field name made lowercase.
    weeknumberofyear = models.SmallIntegerField(db_column='WeekNumberOfYear')  # Field name made lowercase.
    englishmonthname = models.CharField(db_column='EnglishMonthName', max_length=10)  # Field name made lowercase.
    spanishmonthname = models.CharField(db_column='SpanishMonthName', max_length=10)  # Field name made lowercase.
    frenchmonthname = models.CharField(db_column='FrenchMonthName', max_length=10)  # Field name made lowercase.
    monthnumberofyear = models.SmallIntegerField(db_column='MonthNumberOfYear')  # Field name made lowercase.
    calendarquarter = models.SmallIntegerField(db_column='CalendarQuarter')  # Field name made lowercase.
    calendaryear = models.SmallIntegerField(db_column='CalendarYear')  # Field name made lowercase.
    calendarsemester = models.SmallIntegerField(db_column='CalendarSemester')  # Field name made lowercase.
    fiscalquarter = models.SmallIntegerField(db_column='FiscalQuarter')  # Field name made lowercase.
    fiscalyear = models.SmallIntegerField(db_column='FiscalYear')  # Field name made lowercase.
    fiscalsemester = models.SmallIntegerField(db_column='FiscalSemester')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DimDate'


class Dimdepartmentgroup(models.Model):
    departmentgroupkey = models.AutoField(db_column='DepartmentGroupKey', primary_key=True)  # Field name made lowercase.
    parentdepartmentgroupkey = models.ForeignKey('self', models.DO_NOTHING, db_column='ParentDepartmentGroupKey', blank=True, null=True)  # Field name made lowercase.
    departmentgroupname = models.CharField(db_column='DepartmentGroupName', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DimDepartmentGroup'


class Dimemployee(models.Model):
    employeekey = models.AutoField(db_column='EmployeeKey', primary_key=True)  # Field name made lowercase.
    parentemployeekey = models.ForeignKey('self', models.DO_NOTHING, db_column='ParentEmployeeKey', blank=True, null=True)  # Field name made lowercase.
    employeenationalidalternatekey = models.CharField(db_column='EmployeeNationalIDAlternateKey', max_length=15, blank=True, null=True)  # Field name made lowercase.
    parentemployeenationalidalternatekey = models.CharField(db_column='ParentEmployeeNationalIDAlternateKey', max_length=15, blank=True, null=True)  # Field name made lowercase.
    salesterritorykey = models.ForeignKey('Dimsalesterritory', models.DO_NOTHING, db_column='SalesTerritoryKey', blank=True, null=True)  # Field name made lowercase.
    firstname = models.CharField(db_column='FirstName', max_length=50)  # Field name made lowercase.
    lastname = models.CharField(db_column='LastName', max_length=50)  # Field name made lowercase.
    middlename = models.CharField(db_column='MiddleName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    namestyle = models.BooleanField(db_column='NameStyle')  # Field name made lowercase.
    title = models.CharField(db_column='Title', max_length=50, blank=True, null=True)  # Field name made lowercase.
    hiredate = models.DateField(db_column='HireDate', blank=True, null=True)  # Field name made lowercase.
    birthdate = models.DateField(db_column='BirthDate', blank=True, null=True)  # Field name made lowercase.
    loginid = models.CharField(db_column='LoginID', max_length=256, blank=True, null=True)  # Field name made lowercase.
    emailaddress = models.CharField(db_column='EmailAddress', max_length=50, blank=True, null=True)  # Field name made lowercase.
    phone = models.CharField(db_column='Phone', max_length=25, blank=True, null=True)  # Field name made lowercase.
    maritalstatus = models.CharField(db_column='MaritalStatus', max_length=1, blank=True, null=True)  # Field name made lowercase.
    emergencycontactname = models.CharField(db_column='EmergencyContactName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    emergencycontactphone = models.CharField(db_column='EmergencyContactPhone', max_length=25, blank=True, null=True)  # Field name made lowercase.
    salariedflag = models.NullBooleanField(db_column='SalariedFlag')  # Field name made lowercase.
    gender = models.CharField(db_column='Gender', max_length=1, blank=True, null=True)  # Field name made lowercase.
    payfrequency = models.SmallIntegerField(db_column='PayFrequency', blank=True, null=True)  # Field name made lowercase.
    baserate = models.DecimalField(db_column='BaseRate', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    vacationhours = models.SmallIntegerField(db_column='VacationHours', blank=True, null=True)  # Field name made lowercase.
    sickleavehours = models.SmallIntegerField(db_column='SickLeaveHours', blank=True, null=True)  # Field name made lowercase.
    currentflag = models.BooleanField(db_column='CurrentFlag')  # Field name made lowercase.
    salespersonflag = models.BooleanField(db_column='SalesPersonFlag')  # Field name made lowercase.
    departmentname = models.CharField(db_column='DepartmentName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    startdate = models.DateField(db_column='StartDate', blank=True, null=True)  # Field name made lowercase.
    enddate = models.DateField(db_column='EndDate', blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=50, blank=True, null=True)  # Field name made lowercase.
    employeephoto = models.BinaryField(db_column='EmployeePhoto', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DimEmployee'


class Dimgeography(models.Model):
    geographykey = models.AutoField(db_column='GeographyKey', primary_key=True)  # Field name made lowercase.
    city = models.CharField(db_column='City', max_length=30, blank=True, null=True)  # Field name made lowercase.
    stateprovincecode = models.CharField(db_column='StateProvinceCode', max_length=3, blank=True, null=True)  # Field name made lowercase.
    stateprovincename = models.CharField(db_column='StateProvinceName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    countryregioncode = models.CharField(db_column='CountryRegionCode', max_length=3, blank=True, null=True)  # Field name made lowercase.
    englishcountryregionname = models.CharField(db_column='EnglishCountryRegionName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    spanishcountryregionname = models.CharField(db_column='SpanishCountryRegionName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    frenchcountryregionname = models.CharField(db_column='FrenchCountryRegionName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    postalcode = models.CharField(db_column='PostalCode', max_length=15, blank=True, null=True)  # Field name made lowercase.
    salesterritorykey = models.ForeignKey('Dimsalesterritory', models.DO_NOTHING, db_column='SalesTerritoryKey', blank=True, null=True)  # Field name made lowercase.
    ipaddresslocator = models.CharField(db_column='IpAddressLocator', max_length=15, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DimGeography'


class Dimorganization(models.Model):
    organizationkey = models.AutoField(db_column='OrganizationKey', primary_key=True)  # Field name made lowercase.
    parentorganizationkey = models.ForeignKey('self', models.DO_NOTHING, db_column='ParentOrganizationKey', blank=True, null=True)  # Field name made lowercase.
    percentageofownership = models.CharField(db_column='PercentageOfOwnership', max_length=16, blank=True, null=True)  # Field name made lowercase.
    organizationname = models.CharField(db_column='OrganizationName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    currencykey = models.ForeignKey(Dimcurrency, models.DO_NOTHING, db_column='CurrencyKey', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DimOrganization'


class Dimproduct(models.Model):
    productkey = models.AutoField(db_column='ProductKey', primary_key=True)  # Field name made lowercase.
    productalternatekey = models.CharField(db_column='ProductAlternateKey', max_length=25, blank=True, null=True)  # Field name made lowercase.
    productsubcategorykey = models.ForeignKey('Dimproductsubcategory', models.DO_NOTHING, db_column='ProductSubcategoryKey', blank=True, null=True)  # Field name made lowercase.
    weightunitmeasurecode = models.CharField(db_column='WeightUnitMeasureCode', max_length=3, blank=True, null=True)  # Field name made lowercase.
    sizeunitmeasurecode = models.CharField(db_column='SizeUnitMeasureCode', max_length=3, blank=True, null=True)  # Field name made lowercase.
    englishproductname = models.CharField(db_column='EnglishProductName', max_length=50)  # Field name made lowercase.
    spanishproductname = models.CharField(db_column='SpanishProductName', max_length=50)  # Field name made lowercase.
    frenchproductname = models.CharField(db_column='FrenchProductName', max_length=50)  # Field name made lowercase.
    standardcost = models.DecimalField(db_column='StandardCost', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    finishedgoodsflag = models.BooleanField(db_column='FinishedGoodsFlag')  # Field name made lowercase.
    color = models.CharField(db_column='Color', max_length=15)  # Field name made lowercase.
    safetystocklevel = models.SmallIntegerField(db_column='SafetyStockLevel', blank=True, null=True)  # Field name made lowercase.
    reorderpoint = models.SmallIntegerField(db_column='ReorderPoint', blank=True, null=True)  # Field name made lowercase.
    listprice = models.DecimalField(db_column='ListPrice', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    size = models.CharField(db_column='Size', max_length=50, blank=True, null=True)  # Field name made lowercase.
    sizerange = models.CharField(db_column='SizeRange', max_length=50, blank=True, null=True)  # Field name made lowercase.
    weight = models.FloatField(db_column='Weight', blank=True, null=True)  # Field name made lowercase.
    daystomanufacture = models.IntegerField(db_column='DaysToManufacture', blank=True, null=True)  # Field name made lowercase.
    productline = models.CharField(db_column='ProductLine', max_length=2, blank=True, null=True)  # Field name made lowercase.
    dealerprice = models.DecimalField(db_column='DealerPrice', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    class_field = models.CharField(db_column='Class', max_length=2, blank=True, null=True)  # Field name made lowercase. Field renamed because it was a Python reserved word.
    style = models.CharField(db_column='Style', max_length=2, blank=True, null=True)  # Field name made lowercase.
    modelname = models.CharField(db_column='ModelName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    largephoto = models.BinaryField(db_column='LargePhoto', blank=True, null=True)  # Field name made lowercase.
    englishdescription = models.CharField(db_column='EnglishDescription', max_length=400, blank=True, null=True)  # Field name made lowercase.
    frenchdescription = models.CharField(db_column='FrenchDescription', max_length=400, blank=True, null=True)  # Field name made lowercase.
    chinesedescription = models.CharField(db_column='ChineseDescription', max_length=400, blank=True, null=True)  # Field name made lowercase.
    arabicdescription = models.CharField(db_column='ArabicDescription', max_length=400, blank=True, null=True)  # Field name made lowercase.
    hebrewdescription = models.CharField(db_column='HebrewDescription', max_length=400, blank=True, null=True)  # Field name made lowercase.
    thaidescription = models.CharField(db_column='ThaiDescription', max_length=400, blank=True, null=True)  # Field name made lowercase.
    germandescription = models.CharField(db_column='GermanDescription', max_length=400, blank=True, null=True)  # Field name made lowercase.
    japanesedescription = models.CharField(db_column='JapaneseDescription', max_length=400, blank=True, null=True)  # Field name made lowercase.
    turkishdescription = models.CharField(db_column='TurkishDescription', max_length=400, blank=True, null=True)  # Field name made lowercase.
    startdate = models.DateTimeField(db_column='StartDate', blank=True, null=True)  # Field name made lowercase.
    enddate = models.DateTimeField(db_column='EndDate', blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=7, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DimProduct'
        unique_together = (('productalternatekey', 'startdate'),)


class Dimproductcategory(models.Model):
    productcategorykey = models.AutoField(db_column='ProductCategoryKey', primary_key=True)  # Field name made lowercase.
    productcategoryalternatekey = models.IntegerField(db_column='ProductCategoryAlternateKey', unique=True, blank=True, null=True)  # Field name made lowercase.
    englishproductcategoryname = models.CharField(db_column='EnglishProductCategoryName', max_length=50)  # Field name made lowercase.
    spanishproductcategoryname = models.CharField(db_column='SpanishProductCategoryName', max_length=50)  # Field name made lowercase.
    frenchproductcategoryname = models.CharField(db_column='FrenchProductCategoryName', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DimProductCategory'


class Dimproductsubcategory(models.Model):
    productsubcategorykey = models.AutoField(db_column='ProductSubcategoryKey', primary_key=True)  # Field name made lowercase.
    productsubcategoryalternatekey = models.IntegerField(db_column='ProductSubcategoryAlternateKey', unique=True, blank=True, null=True)  # Field name made lowercase.
    englishproductsubcategoryname = models.CharField(db_column='EnglishProductSubcategoryName', max_length=50)  # Field name made lowercase.
    spanishproductsubcategoryname = models.CharField(db_column='SpanishProductSubcategoryName', max_length=50)  # Field name made lowercase.
    frenchproductsubcategoryname = models.CharField(db_column='FrenchProductSubcategoryName', max_length=50)  # Field name made lowercase.
    productcategorykey = models.ForeignKey(Dimproductcategory, models.DO_NOTHING, db_column='ProductCategoryKey', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DimProductSubcategory'


class Dimpromotion(models.Model):
    promotionkey = models.AutoField(db_column='PromotionKey', primary_key=True)  # Field name made lowercase.
    promotionalternatekey = models.IntegerField(db_column='PromotionAlternateKey', unique=True, blank=True, null=True)  # Field name made lowercase.
    englishpromotionname = models.CharField(db_column='EnglishPromotionName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    spanishpromotionname = models.CharField(db_column='SpanishPromotionName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    frenchpromotionname = models.CharField(db_column='FrenchPromotionName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    discountpct = models.FloatField(db_column='DiscountPct', blank=True, null=True)  # Field name made lowercase.
    englishpromotiontype = models.CharField(db_column='EnglishPromotionType', max_length=50, blank=True, null=True)  # Field name made lowercase.
    spanishpromotiontype = models.CharField(db_column='SpanishPromotionType', max_length=50, blank=True, null=True)  # Field name made lowercase.
    frenchpromotiontype = models.CharField(db_column='FrenchPromotionType', max_length=50, blank=True, null=True)  # Field name made lowercase.
    englishpromotioncategory = models.CharField(db_column='EnglishPromotionCategory', max_length=50, blank=True, null=True)  # Field name made lowercase.
    spanishpromotioncategory = models.CharField(db_column='SpanishPromotionCategory', max_length=50, blank=True, null=True)  # Field name made lowercase.
    frenchpromotioncategory = models.CharField(db_column='FrenchPromotionCategory', max_length=50, blank=True, null=True)  # Field name made lowercase.
    startdate = models.DateTimeField(db_column='StartDate')  # Field name made lowercase.
    enddate = models.DateTimeField(db_column='EndDate', blank=True, null=True)  # Field name made lowercase.
    minqty = models.IntegerField(db_column='MinQty', blank=True, null=True)  # Field name made lowercase.
    maxqty = models.IntegerField(db_column='MaxQty', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DimPromotion'


class Dimreseller(models.Model):
    resellerkey = models.AutoField(db_column='ResellerKey', primary_key=True)  # Field name made lowercase.
    geographykey = models.ForeignKey(Dimgeography, models.DO_NOTHING, db_column='GeographyKey', blank=True, null=True)  # Field name made lowercase.
    reselleralternatekey = models.CharField(db_column='ResellerAlternateKey', unique=True, max_length=15, blank=True, null=True)  # Field name made lowercase.
    phone = models.CharField(db_column='Phone', max_length=25, blank=True, null=True)  # Field name made lowercase.
    businesstype = models.CharField(db_column='BusinessType', max_length=20)  # Field name made lowercase.
    resellername = models.CharField(db_column='ResellerName', max_length=50)  # Field name made lowercase.
    numberemployees = models.IntegerField(db_column='NumberEmployees', blank=True, null=True)  # Field name made lowercase.
    orderfrequency = models.CharField(db_column='OrderFrequency', max_length=1, blank=True, null=True)  # Field name made lowercase.
    ordermonth = models.SmallIntegerField(db_column='OrderMonth', blank=True, null=True)  # Field name made lowercase.
    firstorderyear = models.IntegerField(db_column='FirstOrderYear', blank=True, null=True)  # Field name made lowercase.
    lastorderyear = models.IntegerField(db_column='LastOrderYear', blank=True, null=True)  # Field name made lowercase.
    productline = models.CharField(db_column='ProductLine', max_length=50, blank=True, null=True)  # Field name made lowercase.
    addressline1 = models.CharField(db_column='AddressLine1', max_length=60, blank=True, null=True)  # Field name made lowercase.
    addressline2 = models.CharField(db_column='AddressLine2', max_length=60, blank=True, null=True)  # Field name made lowercase.
    annualsales = models.DecimalField(db_column='AnnualSales', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    bankname = models.CharField(db_column='BankName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    minpaymenttype = models.SmallIntegerField(db_column='MinPaymentType', blank=True, null=True)  # Field name made lowercase.
    minpaymentamount = models.DecimalField(db_column='MinPaymentAmount', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    annualrevenue = models.DecimalField(db_column='AnnualRevenue', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    yearopened = models.IntegerField(db_column='YearOpened', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DimReseller'


class Dimsalesreason(models.Model):
    salesreasonkey = models.AutoField(db_column='SalesReasonKey', primary_key=True)  # Field name made lowercase.
    salesreasonalternatekey = models.IntegerField(db_column='SalesReasonAlternateKey')  # Field name made lowercase.
    salesreasonname = models.CharField(db_column='SalesReasonName', max_length=50)  # Field name made lowercase.
    salesreasonreasontype = models.CharField(db_column='SalesReasonReasonType', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DimSalesReason'


class Dimsalesterritory(models.Model):
    salesterritorykey = models.AutoField(db_column='SalesTerritoryKey', primary_key=True)  # Field name made lowercase.
    salesterritoryalternatekey = models.IntegerField(db_column='SalesTerritoryAlternateKey', unique=True, blank=True, null=True)  # Field name made lowercase.
    salesterritoryregion = models.CharField(db_column='SalesTerritoryRegion', max_length=50)  # Field name made lowercase.
    salesterritorycountry = models.CharField(db_column='SalesTerritoryCountry', max_length=50)  # Field name made lowercase.
    salesterritorygroup = models.CharField(db_column='SalesTerritoryGroup', max_length=50, blank=True, null=True)  # Field name made lowercase.
    salesterritoryimage = models.BinaryField(db_column='SalesTerritoryImage', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DimSalesTerritory'


class Dimscenario(models.Model):
    scenariokey = models.AutoField(db_column='ScenarioKey', primary_key=True)  # Field name made lowercase.
    scenarioname = models.CharField(db_column='ScenarioName', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DimScenario'


class Factadditionalinternationalproductdescription(models.Model):
    productkey = models.IntegerField(db_column='ProductKey', primary_key=True)  # Field name made lowercase.
    culturename = models.CharField(db_column='CultureName', max_length=50)  # Field name made lowercase.
    productdescription = models.TextField(db_column='ProductDescription')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'FactAdditionalInternationalProductDescription'
        unique_together = (('productkey', 'culturename'),)


class Factcallcenter(models.Model):
    factcallcenterid = models.AutoField(db_column='FactCallCenterID', primary_key=True)  # Field name made lowercase.
    datekey = models.ForeignKey(Dimdate, models.DO_NOTHING, db_column='DateKey')  # Field name made lowercase.
    wagetype = models.CharField(db_column='WageType', max_length=15)  # Field name made lowercase.
    shift = models.CharField(db_column='Shift', max_length=20)  # Field name made lowercase.
    leveloneoperators = models.SmallIntegerField(db_column='LevelOneOperators')  # Field name made lowercase.
    leveltwooperators = models.SmallIntegerField(db_column='LevelTwoOperators')  # Field name made lowercase.
    totaloperators = models.SmallIntegerField(db_column='TotalOperators')  # Field name made lowercase.
    calls = models.IntegerField(db_column='Calls')  # Field name made lowercase.
    automaticresponses = models.IntegerField(db_column='AutomaticResponses')  # Field name made lowercase.
    orders = models.IntegerField(db_column='Orders')  # Field name made lowercase.
    issuesraised = models.SmallIntegerField(db_column='IssuesRaised')  # Field name made lowercase.
    averagetimeperissue = models.SmallIntegerField(db_column='AverageTimePerIssue')  # Field name made lowercase.
    servicegrade = models.FloatField(db_column='ServiceGrade')  # Field name made lowercase.
    date = models.DateTimeField(db_column='Date', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'FactCallCenter'
        unique_together = (('datekey', 'shift'),)


class Factcurrencyrate(models.Model):
    currencykey = models.ForeignKey(Dimcurrency, models.DO_NOTHING, db_column='CurrencyKey', primary_key=True)  # Field name made lowercase.
    datekey = models.ForeignKey(Dimdate, models.DO_NOTHING, db_column='DateKey')  # Field name made lowercase.
    averagerate = models.FloatField(db_column='AverageRate')  # Field name made lowercase.
    endofdayrate = models.FloatField(db_column='EndOfDayRate')  # Field name made lowercase.
    date = models.DateTimeField(db_column='Date', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'FactCurrencyRate'
        unique_together = (('currencykey', 'datekey'),)


class Factfinance(models.Model):
    financekey = models.AutoField(db_column='FinanceKey', primary_key=True)  # Field name made lowercase.
    datekey = models.ForeignKey(Dimdate, models.DO_NOTHING, db_column='DateKey')  # Field name made lowercase.
    organizationkey = models.ForeignKey(Dimorganization, models.DO_NOTHING, db_column='OrganizationKey')  # Field name made lowercase.
    departmentgroupkey = models.ForeignKey(Dimdepartmentgroup, models.DO_NOTHING, db_column='DepartmentGroupKey')  # Field name made lowercase.
    scenariokey = models.ForeignKey(Dimscenario, models.DO_NOTHING, db_column='ScenarioKey')  # Field name made lowercase.
    accountkey = models.ForeignKey(Dimaccount, models.DO_NOTHING, db_column='AccountKey')  # Field name made lowercase.
    amount = models.FloatField(db_column='Amount')  # Field name made lowercase.
    date = models.DateTimeField(db_column='Date', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'FactFinance'


class Factinternetsales(models.Model):
    productkey = models.ForeignKey(Dimproduct, models.DO_NOTHING, db_column='ProductKey')  # Field name made lowercase.
    orderdatekey = models.ForeignKey(Dimdate, models.DO_NOTHING, db_column='OrderDateKey', related_name="FactinternetsalesByOrderdatekey")  # Field name made lowercase.
    duedatekey = models.ForeignKey(Dimdate, models.DO_NOTHING, db_column='DueDateKey', related_name="FactinternetsalesByDuedatekey")  # Field name made lowercase.
    shipdatekey = models.ForeignKey(Dimdate, models.DO_NOTHING, db_column='ShipDateKey', related_name="FactinternetsalesByShipdatekey")  # Field name made lowercase.
    customerkey = models.ForeignKey(Dimcustomer, models.DO_NOTHING, db_column='CustomerKey')  # Field name made lowercase.
    promotionkey = models.ForeignKey(Dimpromotion, models.DO_NOTHING, db_column='PromotionKey')  # Field name made lowercase.
    currencykey = models.ForeignKey(Dimcurrency, models.DO_NOTHING, db_column='CurrencyKey')  # Field name made lowercase.
    salesterritorykey = models.ForeignKey(Dimsalesterritory, models.DO_NOTHING, db_column='SalesTerritoryKey')  # Field name made lowercase.
    salesordernumber = models.CharField(db_column='SalesOrderNumber', primary_key=True, max_length=20)  # Field name made lowercase.
    salesorderlinenumber = models.SmallIntegerField(db_column='SalesOrderLineNumber')  # Field name made lowercase.
    revisionnumber = models.SmallIntegerField(db_column='RevisionNumber')  # Field name made lowercase.
    orderquantity = models.SmallIntegerField(db_column='OrderQuantity')  # Field name made lowercase.
    unitprice = models.DecimalField(db_column='UnitPrice', max_digits=19, decimal_places=4)  # Field name made lowercase.
    extendedamount = models.DecimalField(db_column='ExtendedAmount', max_digits=19, decimal_places=4)  # Field name made lowercase.
    unitpricediscountpct = models.FloatField(db_column='UnitPriceDiscountPct')  # Field name made lowercase.
    discountamount = models.FloatField(db_column='DiscountAmount')  # Field name made lowercase.
    productstandardcost = models.DecimalField(db_column='ProductStandardCost', max_digits=19, decimal_places=4)  # Field name made lowercase.
    totalproductcost = models.DecimalField(db_column='TotalProductCost', max_digits=19, decimal_places=4)  # Field name made lowercase.
    salesamount = models.DecimalField(db_column='SalesAmount', max_digits=19, decimal_places=4)  # Field name made lowercase.
    taxamt = models.DecimalField(db_column='TaxAmt', max_digits=19, decimal_places=4)  # Field name made lowercase.
    freight = models.DecimalField(db_column='Freight', max_digits=19, decimal_places=4)  # Field name made lowercase.
    carriertrackingnumber = models.CharField(db_column='CarrierTrackingNumber', max_length=25, blank=True, null=True)  # Field name made lowercase.
    customerponumber = models.CharField(db_column='CustomerPONumber', max_length=25, blank=True, null=True)  # Field name made lowercase.
    orderdate = models.DateTimeField(db_column='OrderDate', blank=True, null=True)  # Field name made lowercase.
    duedate = models.DateTimeField(db_column='DueDate', blank=True, null=True)  # Field name made lowercase.
    shipdate = models.DateTimeField(db_column='ShipDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'FactInternetSales'
        unique_together = (('salesordernumber', 'salesorderlinenumber'),)


class Factinternetsalesreason(models.Model):
    salesordernumber = models.ForeignKey(Factinternetsales, models.DO_NOTHING, db_column='SalesOrderNumber', primary_key=True, related_name="FactinternetsalesreasonBySalesordernumber")  # Field name made lowercase.
    salesorderlinenumber = models.ForeignKey(Factinternetsales, models.DO_NOTHING, db_column='SalesOrderLineNumber', related_name="FactinternetsalesreasonBySalesorderlinenumber")  # Field name made lowercase.
    salesreasonkey = models.ForeignKey(Dimsalesreason, models.DO_NOTHING, db_column='SalesReasonKey')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'FactInternetSalesReason'
        unique_together = (('salesordernumber', 'salesorderlinenumber', 'salesreasonkey'),)


class Factproductinventory(models.Model):
    productkey = models.ForeignKey(Dimproduct, models.DO_NOTHING, db_column='ProductKey', primary_key=True)  # Field name made lowercase.
    datekey = models.ForeignKey(Dimdate, models.DO_NOTHING, db_column='DateKey')  # Field name made lowercase.
    movementdate = models.DateField(db_column='MovementDate')  # Field name made lowercase.
    unitcost = models.DecimalField(db_column='UnitCost', max_digits=19, decimal_places=4)  # Field name made lowercase.
    unitsin = models.IntegerField(db_column='UnitsIn')  # Field name made lowercase.
    unitsout = models.IntegerField(db_column='UnitsOut')  # Field name made lowercase.
    unitsbalance = models.IntegerField(db_column='UnitsBalance')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'FactProductInventory'
        unique_together = (('productkey', 'datekey'),)


class Factresellersales(models.Model):
    productkey = models.ForeignKey(Dimproduct, models.DO_NOTHING, db_column='ProductKey')  # Field name made lowercase.
    orderdatekey = models.ForeignKey(Dimdate, models.DO_NOTHING, db_column='OrderDateKey', related_name="FactresellersalesByOrderdatakey")  # Field name made lowercase.
    duedatekey = models.ForeignKey(Dimdate, models.DO_NOTHING, db_column='DueDateKey', related_name="FactresellersalesByDuedatakey")  # Field name made lowercase.
    shipdatekey = models.ForeignKey(Dimdate, models.DO_NOTHING, db_column='ShipDateKey', related_name="FactresellersalesByShipdatakey")  # Field name made lowercase.
    resellerkey = models.ForeignKey(Dimreseller, models.DO_NOTHING, db_column='ResellerKey')  # Field name made lowercase.
    employeekey = models.ForeignKey(Dimemployee, models.DO_NOTHING, db_column='EmployeeKey')  # Field name made lowercase.
    promotionkey = models.ForeignKey(Dimpromotion, models.DO_NOTHING, db_column='PromotionKey')  # Field name made lowercase.
    currencykey = models.ForeignKey(Dimcurrency, models.DO_NOTHING, db_column='CurrencyKey')  # Field name made lowercase.
    salesterritorykey = models.ForeignKey(Dimsalesterritory, models.DO_NOTHING, db_column='SalesTerritoryKey')  # Field name made lowercase.
    salesordernumber = models.CharField(db_column='SalesOrderNumber', primary_key=True, max_length=20)  # Field name made lowercase.
    salesorderlinenumber = models.SmallIntegerField(db_column='SalesOrderLineNumber')  # Field name made lowercase.
    revisionnumber = models.SmallIntegerField(db_column='RevisionNumber', blank=True, null=True)  # Field name made lowercase.
    orderquantity = models.SmallIntegerField(db_column='OrderQuantity', blank=True, null=True)  # Field name made lowercase.
    unitprice = models.DecimalField(db_column='UnitPrice', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    extendedamount = models.DecimalField(db_column='ExtendedAmount', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    unitpricediscountpct = models.FloatField(db_column='UnitPriceDiscountPct', blank=True, null=True)  # Field name made lowercase.
    discountamount = models.FloatField(db_column='DiscountAmount', blank=True, null=True)  # Field name made lowercase.
    productstandardcost = models.DecimalField(db_column='ProductStandardCost', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    totalproductcost = models.DecimalField(db_column='TotalProductCost', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    salesamount = models.DecimalField(db_column='SalesAmount', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    taxamt = models.DecimalField(db_column='TaxAmt', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    freight = models.DecimalField(db_column='Freight', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    carriertrackingnumber = models.CharField(db_column='CarrierTrackingNumber', max_length=25, blank=True, null=True)  # Field name made lowercase.
    customerponumber = models.CharField(db_column='CustomerPONumber', max_length=25, blank=True, null=True)  # Field name made lowercase.
    orderdate = models.DateTimeField(db_column='OrderDate', blank=True, null=True)  # Field name made lowercase.
    duedate = models.DateTimeField(db_column='DueDate', blank=True, null=True)  # Field name made lowercase.
    shipdate = models.DateTimeField(db_column='ShipDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'FactResellerSales'
        unique_together = (('salesordernumber', 'salesorderlinenumber'),)


class Factsalesquota(models.Model):
    salesquotakey = models.AutoField(db_column='SalesQuotaKey', primary_key=True)  # Field name made lowercase.
    employeekey = models.ForeignKey(Dimemployee, models.DO_NOTHING, db_column='EmployeeKey')  # Field name made lowercase.
    datekey = models.ForeignKey(Dimdate, models.DO_NOTHING, db_column='DateKey')  # Field name made lowercase.
    calendaryear = models.SmallIntegerField(db_column='CalendarYear')  # Field name made lowercase.
    calendarquarter = models.SmallIntegerField(db_column='CalendarQuarter')  # Field name made lowercase.
    salesamountquota = models.DecimalField(db_column='SalesAmountQuota', max_digits=19, decimal_places=4)  # Field name made lowercase.
    date = models.DateTimeField(db_column='Date', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'FactSalesQuota'


class Factsurveyresponse(models.Model):
    surveyresponsekey = models.AutoField(db_column='SurveyResponseKey', primary_key=True)  # Field name made lowercase.
    datekey = models.ForeignKey(Dimdate, models.DO_NOTHING, db_column='DateKey')  # Field name made lowercase.
    customerkey = models.ForeignKey(Dimcustomer, models.DO_NOTHING, db_column='CustomerKey')  # Field name made lowercase.
    productcategorykey = models.IntegerField(db_column='ProductCategoryKey')  # Field name made lowercase.
    englishproductcategoryname = models.CharField(db_column='EnglishProductCategoryName', max_length=50)  # Field name made lowercase.
    productsubcategorykey = models.IntegerField(db_column='ProductSubcategoryKey')  # Field name made lowercase.
    englishproductsubcategoryname = models.CharField(db_column='EnglishProductSubcategoryName', max_length=50)  # Field name made lowercase.
    date = models.DateTimeField(db_column='Date', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'FactSurveyResponse'


class Newfactcurrencyrate(models.Model):
    averagerate = models.FloatField(db_column='AverageRate', blank=True, null=True)  # Field name made lowercase.
    currencyid = models.CharField(db_column='CurrencyID', max_length=3, blank=True, null=True)  # Field name made lowercase.
    currencydate = models.DateField(db_column='CurrencyDate', blank=True, null=True)  # Field name made lowercase.
    endofdayrate = models.FloatField(db_column='EndOfDayRate', blank=True, null=True)  # Field name made lowercase.
    currencykey = models.IntegerField(db_column='CurrencyKey', blank=True, null=True)  # Field name made lowercase.
    datekey = models.IntegerField(db_column='DateKey', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'NewFactCurrencyRate'


class Prospectivebuyer(models.Model):
    prospectivebuyerkey = models.AutoField(db_column='ProspectiveBuyerKey', primary_key=True)  # Field name made lowercase.
    prospectalternatekey = models.CharField(db_column='ProspectAlternateKey', max_length=15, blank=True, null=True)  # Field name made lowercase.
    firstname = models.CharField(db_column='FirstName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    middlename = models.CharField(db_column='MiddleName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    lastname = models.CharField(db_column='LastName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    birthdate = models.DateTimeField(db_column='BirthDate', blank=True, null=True)  # Field name made lowercase.
    maritalstatus = models.CharField(db_column='MaritalStatus', max_length=1, blank=True, null=True)  # Field name made lowercase.
    gender = models.CharField(db_column='Gender', max_length=1, blank=True, null=True)  # Field name made lowercase.
    emailaddress = models.CharField(db_column='EmailAddress', max_length=50, blank=True, null=True)  # Field name made lowercase.
    yearlyincome = models.DecimalField(db_column='YearlyIncome', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    totalchildren = models.SmallIntegerField(db_column='TotalChildren', blank=True, null=True)  # Field name made lowercase.
    numberchildrenathome = models.SmallIntegerField(db_column='NumberChildrenAtHome', blank=True, null=True)  # Field name made lowercase.
    education = models.CharField(db_column='Education', max_length=40, blank=True, null=True)  # Field name made lowercase.
    occupation = models.CharField(db_column='Occupation', max_length=100, blank=True, null=True)  # Field name made lowercase.
    houseownerflag = models.CharField(db_column='HouseOwnerFlag', max_length=1, blank=True, null=True)  # Field name made lowercase.
    numbercarsowned = models.SmallIntegerField(db_column='NumberCarsOwned', blank=True, null=True)  # Field name made lowercase.
    addressline1 = models.CharField(db_column='AddressLine1', max_length=120, blank=True, null=True)  # Field name made lowercase.
    addressline2 = models.CharField(db_column='AddressLine2', max_length=120, blank=True, null=True)  # Field name made lowercase.
    city = models.CharField(db_column='City', max_length=30, blank=True, null=True)  # Field name made lowercase.
    stateprovincecode = models.CharField(db_column='StateProvinceCode', max_length=3, blank=True, null=True)  # Field name made lowercase.
    postalcode = models.CharField(db_column='PostalCode', max_length=15, blank=True, null=True)  # Field name made lowercase.
    phone = models.CharField(db_column='Phone', max_length=20, blank=True, null=True)  # Field name made lowercase.
    salutation = models.CharField(db_column='Salutation', max_length=8, blank=True, null=True)  # Field name made lowercase.
    unknown = models.IntegerField(db_column='Unknown', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ProspectiveBuyer'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Sysdiagrams(models.Model):
    name = models.CharField(max_length=128)
    principal_id = models.IntegerField()
    diagram_id = models.AutoField(primary_key=True)
    version = models.IntegerField(blank=True, null=True)
    definition = models.BinaryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sysdiagrams'
        unique_together = (('principal_id', 'name'),)
