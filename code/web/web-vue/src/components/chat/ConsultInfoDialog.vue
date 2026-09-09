<template>
  <el-dialog
    :model-value="visible"
    title="新建问诊"
    width="560px"
    :close-on-click-modal="false"
    @update:model-value="onVisibleChange"
    @closed="resetForm"
  >
    <el-alert
      title="请填写患者基础信息，这些信息会随每次提问作为智能诊断的参考背景，可让 AI 给出更贴合患者情况的建议。"
      type="info"
      :closable="false"
      show-icon
      style="margin-bottom: 16px;"
    />

    <el-form ref="formRef" :model="form" :rules="rules" label-width="100px">
      <el-form-item label="问诊名称" prop="consultName">
        <el-input v-model="form.consultName" placeholder="如：高血压复诊咨询" maxlength="50" show-word-limit />
      </el-form-item>

      <el-row :gutter="16">
        <el-col :span="12">
          <el-form-item label="患者姓名" prop="patientName">
            <el-input v-model="form.patientName" placeholder="请输入患者姓名" maxlength="20" />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="年龄" prop="age">
            <el-input-number v-model="form.age" :min="0" :max="150" placeholder="年龄" style="width: 100%" />
          </el-form-item>
        </el-col>
      </el-row>

      <el-row :gutter="16">
        <el-col :span="12">
          <el-form-item label="性别" prop="gender">
            <el-select v-model="form.gender" placeholder="请选择性别" style="width: 100%">
              <el-option label="男" value="男" />
              <el-option label="女" value="女" />
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="问诊科室" prop="categoryId">
            <el-select v-model="form.categoryId" placeholder="请选择科室" style="width: 100%">
              <el-option
                v-for="cat in categories"
                :key="cat.id"
                :label="cat.name"
                :value="cat.id"
              />
            </el-select>
          </el-form-item>
        </el-col>
      </el-row>

      <el-form-item label="特殊情况备注" prop="remark">
        <el-input
          v-model="form.remark"
          type="textarea"
          :rows="3"
          maxlength="300"
          show-word-limit
          placeholder="如：高血压病史、药物过敏史、正在服用的药物等（选填）"
        />
      </el-form-item>
    </el-form>

    <template #footer>
      <span class="dialog-footer">
        <el-button @click="cancel">取消</el-button>
        <el-button type="primary" :loading="submitting" @click="confirm">开始问诊</el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import type { FormInstance } from 'element-plus'
import type { CategoryVO } from '@/types/item'
import type { ConsultInfo } from '@/types/chat'

const props = defineProps<{
  visible: boolean;
  categories: CategoryVO[];
}>()

const emit = defineEmits<{
  'update:visible': [value: boolean];
  'confirm': [info: ConsultInfo];
  'cancel': [];
}>()

const formRef = ref<FormInstance>()

const form = reactive<ConsultInfo>({
  consultName: '',
  patientName: '',
  age: null,
  gender: '',
  categoryId: null,
  categoryName: '',
  remark: ''
})

const submitting = ref(false)

const rules = {
  consultName: [
    { required: true, message: '请输入问诊名称', trigger: 'blur' }
  ],
  patientName: [
    { required: true, message: '请输入患者姓名', trigger: 'blur' }
  ]
}

const onVisibleChange = (value: boolean) => {
  emit('update:visible', value)
}

const resetForm = () => {
  form.consultName = ''
  form.patientName = ''
  form.age = null
  form.gender = ''
  form.categoryId = null
  form.categoryName = ''
  form.remark = ''
}

const confirm = async () => {
  if (!formRef.value) return
  try {
    await formRef.value.validate()
    const selected = props.categories.find(c => c.id === form.categoryId)
    form.categoryName = selected ? selected.name : ''
    submitting.value = true
    emit('confirm', { ...form })
  } catch (error) {
    console.error('问诊基础信息校验失败:', error)
  } finally {
    submitting.value = false
  }
}

const cancel = () => {
  emit('cancel')
}
</script>
