# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'student'
        db.create_table('student_info_student', (
            ('prn', self.gf('django.db.models.fields.CharField')(unique=True, max_length=12, primary_key=True)),
            ('fullname', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('sex', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=255)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=12, null=True, blank=True)),
            ('career_objective', self.gf('django.db.models.fields.TextField')()),
            ('photo', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('certification', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('project', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('academic', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('extracurricular', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('workex', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('Extra_field', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('last_update', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('student_info', ['student'])

        # Adding model 'marks'
        db.create_table('student_info_marks', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('primary_table', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['student_info.student'])),
            ('course', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('uni', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('marks', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=4, blank=True)),
            ('markstype', self.gf('django.db.models.fields.CharField')(default='Total Score', max_length=15)),
            ('outof', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=4, blank=True)),
            ('fromDate', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal('student_info', ['marks'])

        # Adding model 'personal'
        db.create_table('student_info_personal', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('primary_table', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['student_info.student'], unique=True)),
            ('mother_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('father_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('birthdate', self.gf('django.db.models.fields.DateField')()),
            ('areasofinterest', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
            ('mother_occupation', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('father_occupation', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('languages', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('hobbies', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('strength', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('weakness', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('per_address', self.gf('django.db.models.fields.TextField')(max_length=200)),
            ('corr_address', self.gf('django.db.models.fields.TextField')(max_length=200)),
        ))
        db.send_create_signal('student_info', ['personal'])

        # Adding model 'swExposure'
        db.create_table('student_info_swexposure', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('primary_table', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['student_info.student'])),
            ('programming', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('databases', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('OS', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('swPackages', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('webTools', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('student_info', ['swExposure'])

        # Adding model 'ExtraField'
        db.create_table('student_info_extrafield', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('primary_table', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['student_info.student'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('desc', self.gf('django.db.models.fields.TextField')()),
            ('fromDate', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('endDate', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal('student_info', ['ExtraField'])

        # Adding model 'workex'
        db.create_table('student_info_workex', (
            ('extrafield_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['student_info.ExtraField'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('student_info', ['workex'])

        # Adding model 'certification'
        db.create_table('student_info_certification', (
            ('extrafield_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['student_info.ExtraField'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('student_info', ['certification'])

        # Adding model 'project'
        db.create_table('student_info_project', (
            ('extrafield_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['student_info.ExtraField'], unique=True, primary_key=True)),
            ('heading', self.gf('django.db.models.fields.CharField')(max_length=40, blank=True)),
        ))
        db.send_create_signal('student_info', ['project'])

        # Adding model 'academic'
        db.create_table('student_info_academic', (
            ('extrafield_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['student_info.ExtraField'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('student_info', ['academic'])

        # Adding model 'extracurricular'
        db.create_table('student_info_extracurricular', (
            ('extrafield_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['student_info.ExtraField'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('student_info', ['extracurricular'])

        # Adding model 'AdditionalInfo'
        db.create_table('student_info_additionalinfo', (
            ('extrafield_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['student_info.ExtraField'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('student_info', ['AdditionalInfo'])

        # Adding model 'companySpecific'
        db.create_table('student_info_companyspecific', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fieldType', self.gf('django.db.models.fields.CharField')(default='text', max_length=50)),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('displayText', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('is_mandatory', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('dataType', self.gf('django.db.models.fields.CharField')(default='none', max_length=10)),
            ('createdOn', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('student_info', ['companySpecific'])

        # Adding model 'companySpecificData'
        db.create_table('student_info_companyspecificdata', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('primary_table', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['student_info.student'])),
            ('valueOf', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['student_info.companySpecific'])),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
        ))
        db.send_create_signal('student_info', ['companySpecificData'])


    def backwards(self, orm):
        # Deleting model 'student'
        db.delete_table('student_info_student')

        # Deleting model 'marks'
        db.delete_table('student_info_marks')

        # Deleting model 'personal'
        db.delete_table('student_info_personal')

        # Deleting model 'swExposure'
        db.delete_table('student_info_swexposure')

        # Deleting model 'ExtraField'
        db.delete_table('student_info_extrafield')

        # Deleting model 'workex'
        db.delete_table('student_info_workex')

        # Deleting model 'certification'
        db.delete_table('student_info_certification')

        # Deleting model 'project'
        db.delete_table('student_info_project')

        # Deleting model 'academic'
        db.delete_table('student_info_academic')

        # Deleting model 'extracurricular'
        db.delete_table('student_info_extracurricular')

        # Deleting model 'AdditionalInfo'
        db.delete_table('student_info_additionalinfo')

        # Deleting model 'companySpecific'
        db.delete_table('student_info_companyspecific')

        # Deleting model 'companySpecificData'
        db.delete_table('student_info_companyspecificdata')


    models = {
        'student_info.academic': {
            'Meta': {'object_name': 'academic', '_ormbases': ['student_info.ExtraField']},
            'extrafield_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['student_info.ExtraField']", 'unique': 'True', 'primary_key': 'True'})
        },
        'student_info.additionalinfo': {
            'Meta': {'object_name': 'AdditionalInfo', '_ormbases': ['student_info.ExtraField']},
            'extrafield_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['student_info.ExtraField']", 'unique': 'True', 'primary_key': 'True'})
        },
        'student_info.certification': {
            'Meta': {'object_name': 'certification', '_ormbases': ['student_info.ExtraField']},
            'extrafield_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['student_info.ExtraField']", 'unique': 'True', 'primary_key': 'True'})
        },
        'student_info.companyspecific': {
            'Meta': {'object_name': 'companySpecific'},
            'createdOn': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'dataType': ('django.db.models.fields.CharField', [], {'default': "'none'", 'max_length': '10'}),
            'displayText': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'fieldType': ('django.db.models.fields.CharField', [], {'default': "'text'", 'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_mandatory': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'student_info.companyspecificdata': {
            'Meta': {'object_name': 'companySpecificData'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'primary_table': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['student_info.student']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'valueOf': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['student_info.companySpecific']"})
        },
        'student_info.extracurricular': {
            'Meta': {'object_name': 'extracurricular', '_ormbases': ['student_info.ExtraField']},
            'extrafield_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['student_info.ExtraField']", 'unique': 'True', 'primary_key': 'True'})
        },
        'student_info.extrafield': {
            'Meta': {'object_name': 'ExtraField'},
            'desc': ('django.db.models.fields.TextField', [], {}),
            'endDate': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'fromDate': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'primary_table': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['student_info.student']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'student_info.marks': {
            'Meta': {'object_name': 'marks'},
            'course': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'fromDate': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'marks': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '4', 'blank': 'True'}),
            'markstype': ('django.db.models.fields.CharField', [], {'default': "'Total Score'", 'max_length': '15'}),
            'outof': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '4', 'blank': 'True'}),
            'primary_table': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['student_info.student']"}),
            'uni': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'student_info.personal': {
            'Meta': {'object_name': 'personal'},
            'areasofinterest': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'birthdate': ('django.db.models.fields.DateField', [], {}),
            'corr_address': ('django.db.models.fields.TextField', [], {'max_length': '200'}),
            'father_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'father_occupation': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'hobbies': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'languages': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'mother_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'mother_occupation': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'per_address': ('django.db.models.fields.TextField', [], {'max_length': '200'}),
            'primary_table': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['student_info.student']", 'unique': 'True'}),
            'strength': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'weakness': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'student_info.project': {
            'Meta': {'object_name': 'project', '_ormbases': ['student_info.ExtraField']},
            'extrafield_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['student_info.ExtraField']", 'unique': 'True', 'primary_key': 'True'}),
            'heading': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'})
        },
        'student_info.student': {
            'Extra_field': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'Meta': {'object_name': 'student'},
            'academic': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'career_objective': ('django.db.models.fields.TextField', [], {}),
            'certification': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '255'}),
            'extracurricular': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'fullname': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'last_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '12', 'null': 'True', 'blank': 'True'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'prn': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '12', 'primary_key': 'True'}),
            'project': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sex': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'workex': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'student_info.swexposure': {
            'Meta': {'object_name': 'swExposure'},
            'OS': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'databases': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'primary_table': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['student_info.student']"}),
            'programming': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'swPackages': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'webTools': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'student_info.workex': {
            'Meta': {'object_name': 'workex', '_ormbases': ['student_info.ExtraField']},
            'extrafield_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['student_info.ExtraField']", 'unique': 'True', 'primary_key': 'True'})
        }
    }

    complete_apps = ['student_info']