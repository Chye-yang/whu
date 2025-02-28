from django.db import models
# Create your models here.


class Record(models.Model):
    id = models.AutoField(primary_key=True)
    srcip = models.CharField(max_length=255)
    dstip = models.CharField(max_length=255)
    srcport = models.IntegerField()
    dstport = models.IntegerField()
    proto = models.CharField(max_length=255)
    attack_cat = models.CharField(max_length=255)
    label = models.CharField(max_length=255)

    class Meta:
        db_table = "netlog"


class Library(models.Model):
    id = models.AutoField(primary_key=True)
    attack_reference = models.CharField(max_length=255)
    attack_description = models.CharField(max_length=255)
    attack_time = models.CharField(max_length=255)

    class Meta:
        db_table = "attack_cve"


class Statistic(models.Model):
    id = models.AutoField(primary_key=True)
    proto = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    rate = models.DecimalField(max_digits=15, decimal_places=5)
    sttl = models.IntegerField()
    dttl = models.IntegerField()
    sload = models.IntegerField()
    dload = models.IntegerField()
    sjit = models.DecimalField(max_digits=15, decimal_places=5)
    djit = models.DecimalField(max_digits=15, decimal_places=5)
    attack_cat = models.CharField(max_length=255)
    label = models.CharField(max_length=255)

    class Meta:
        db_table = "tiny-set"




class Analysis(models.Model):
    id = models.AutoField(primary_key=True, null=False, unique=True)
    date = models.CharField(null=False, max_length=255)
    all = models.CharField(null=False, max_length=255)
    tcpv4 = models.CharField(null=False, max_length=255)
    tcpv6 = models.CharField(null=False, max_length=255)
    udpv4 = models.CharField(null=False, max_length=255)
    udpv6 = models.CharField(null=False, max_length=255)
    otherv4 = models.CharField(null=False, max_length=255)
    otherv6 = models.CharField(null=False, max_length=255)

    arp = models.CharField(null=False, max_length=255)
    rarp = models.CharField(null=False, max_length=255)
    other = models.CharField(null=False, max_length=255)
    outFlow = models.CharField(null=False, max_length=255)
    inputFlow = models.CharField(null=False, max_length=255)

    ipv4 = models.CharField(null=False, max_length=255)
    ipv6 = models.CharField(null=False, max_length=255)
    icmpv4 = models.CharField(null=False, max_length=255)
    icmpv6 = models.CharField(null=False, max_length=255)
    uniCast = models.CharField(null=False, max_length=255)
    broadcast = models.CharField(null=False, max_length=255)
    multicast = models.CharField(null=False, max_length=255)

class PortInfo(models.Model):
    id = models.AutoField(primary_key=True, null=False, unique=True)
    no = models.CharField(null=False, max_length=255)
    cur = models.CharField(null=False, max_length=255)
    pre = models.CharField(null=False, max_length=255)
    inFlow = models.CharField(null=False, max_length=255)
    outFlow = models.CharField(null=False, max_length=255)

class Prediction(models.Model):
    id = models.AutoField(primary_key=True, null=False, unique=True)
    city = models.CharField(null=False, max_length=255)
    date = models.CharField(null=False, max_length=255)
    protocol = models.CharField(null=False, max_length=255)
    src_ip = models.CharField(null=False, max_length=255)
    dst_ip = models.CharField(null=False, max_length=255)
    src_port = models.IntegerField(null=False)
    dst_port = models.IntegerField(null=False)
    prob = models.CharField(null=False, max_length=255)
    attack = models.CharField(null=True, max_length=255)
    class Meta:
        db_table = "model_prediction"

class Behavior(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.CharField(max_length=255)
    protocol = models.CharField(max_length=255)
    service = models.CharField(max_length=255)
    src_ip = models.CharField(max_length=255)
    dst_ip = models.CharField(max_length=255)
    behavior_type = models.CharField(max_length=255)
    attack_type = models.CharField(max_length=255)

    class Meta:
        db_table = "behavior"

class Behavior_predict(models.Model):
    id = models.AutoField(primary_key=True)
    bytes = models.CharField(max_length=1024)
    protocol = models.CharField(max_length=1024)
    service = models.CharField(max_length=1024)
    attack_type = models.CharField(max_length=1024)
    behavior_type = models.CharField(max_length=1024)

    class Meta:
        db_table = "behavior_predict"

