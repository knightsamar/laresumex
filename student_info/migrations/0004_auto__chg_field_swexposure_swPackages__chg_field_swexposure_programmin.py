# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'swExposure.swPackages'
        db.alter_column('student_info_swexposure', 'swPackages', self.gf('django.db.models.fields.CharField')(max_length=100, null=True))

        # Changing field 'swExposure.programming'
        db.alter_column('student_info_swexposure', 'programming', self.gf('django.db.models.fields.CharField')(max_length=100, null=True))

        # Changing field 'swExposure.databases'
        db.alter_column('student_info_swexposure', 'databases', self.gf('django.db.models.fields.CharField')(max_length=100, null=True))

        # Changing field 'swExposure.webTools'
        db.alter_column('student_info_swexposure', 'webTools', self.gf('django.db.models.fields.CharField')(max_length=100, null=True))

        # Changing field 'swExposure.OS'
        db.alter_column('student_info_swexposure', 'OS', self.gf('django.db.models.fields.CharField')(max_length=100, null=True))

    def backwards(self, orm):

        # Changing field 'swExposure.swPackages'
        db.alter_column('student_info_swexposure', 'swPackages', self.gf('django.db.models.fields.CharField')(default='', max_length=100))

        # Changing field 'swExposure.programming'
        db.alter_column('student_info_swexposure', 'programming', self.gf('django.db.models.fields.CharField')(default='', max_length=100))

        # Changing field 'swExposure.databases'
        db.alter_column('student_info_swexposure', 'databases', self.gf('django.db.models.fields.CharField')(default='', max_length=100))

        # Changing field 'swExposure.webTools'
        db.alter_column('student_info_swexposure', 'webTools', self.gf('django.db.models.fields.CharField')(default='', max_length=100))

        # Changing field 'swExposure.OS'
        db.alter_column('student_info_swexposure', 'OS', self.gf('django.db.models.fields.CharField')(default='', max_length=100))

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
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
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
            'father_occupation': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'hobbies': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'languages': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'mother_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'mother_occupation': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'per_address': ('django.db.models.fields.TextField', [], {'max_length': '200'}),
            'primary_table': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['student_info.student']", 'unique': 'True'}),
            'strength': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'weakness': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'student_info.project': {
            'Meta': {'object_name': 'project', '_ormbases': ['student_info.ExtraField']},
            'extrafield_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['student_info.ExtraField']", 'unique': 'True', 'primary_key': 'True'}),
            'heading': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
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
            'OS': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'databases': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'primary_table': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['student_info.student']"}),
            'programming': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'swPackages': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'webTools': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'student_info.workex': {
            'Meta': {'object_name': 'workex', '_ormbases': ['student_info.ExtraField']},
            'extrafield_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['student_info.ExtraField']", 'unique': 'True', 'primary_key': 'True'})
        }
    }

    complete_apps = ['student_info']