import axios from 'axios';

const baseURL = 'http://127.0.0.1:5000'; // 后端服务器地址，根据实际情况修改

export const runDirectInference = async (file) => {
  try {
    const formData = new FormData();
    formData.append('file', file);
    console.log('FormData详情,所有键值对:', formData.getAll('file'));
    console.log('FormData详情,查看整体结构:', [...formData.entries()]);
    const response = await axios.post(`${baseURL}/direct-inference`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
    console.log('后端返回的完整响应内容:', response);
    console.log('后端返回的响应数据(response.data):', response.data);
    const responseText = response.data;
    const energyMatch = responseText.match(/CHGNet-predicted energy \(eV\/atom\):\s*([\d.-]+)/);
    const energy = energyMatch? `${energyMatch[1]} eV/atom` : '暂无能量数据';

    const forcesMatch = responseText.match(/CHGNet-predicted forces \(eV\/A\):\s+((?:[^\n]*\n)+)(?=CHGNet-predicted stress \(GPa\):)/);
    console.log('forcesMatch的值:', forcesMatch);
    const forces = forcesMatch? forcesMatch[1].trim().split('\n').map(row => {
      console.log('处理每一行前，当前行的内容:', row);
      if(row === ''){
        return [];
      }
      const rowMatch = row.match(/([\d.-]+)/g);
      console.log('当前行匹配的结果:', rowMatch);
      return rowMatch? rowMatch.map(Number) : [];
    }) : undefined;
   
    const stressMatch = responseText.match(/CHGNet-predicted stress \(GPa\):\s*((?:[^\n]*\n)+)(?=CHGNet-predicted magmom \(mu_B\):)/);
    const stress = stressMatch? stressMatch[1].trim().split('\n').map(row => {
      if (row === '') {
        return []; // 如果是空行，直接返回空数组，跳过这一行继续处理下一行
      }
      // 可以添加更多格式判断逻辑，比如判断是否只包含空格等情况，如果不符合预期格式也返回空数组等处理方式
      console.log('当前正在处理的应力数据行内容:', row);
      const rowMatch = row.match(/\s*([\d.-]+)\s*/g);
      console.log('当前行的匹配结果:', rowMatch);
      return rowMatch? rowMatch.map(Number) : [];
    }) : undefined;

    const magmomMatch = responseText.match(/CHGNet-predicted magmom \(mu_B\):\s*((?:[^\n]*\n)+)(?=\n*$)/);
    const magmom = magmomMatch? magmomMatch[1].trim().split('\n').map(row =>{
      if (row === '') {
        return []; // 如果是空行，直接返回空数组，跳过这一行继续处理下一行
      }
      const rowMatch=row.match(/\s*([\d.-]+)\s*/g);
      return rowMatch? rowMatch.map(Number) : [];
    }) : undefined;

        return {
            energy: energy,
            forces: forces,
            stress: stress,
            magmom: magmom
        };
  } catch (error) {
    console.error('Error running direct inference:', error);
    if (error.response) {
      if (error.response.status === 400) {
          throw new Error('请求格式错误，请检查文件及请求参数是否符合要求。');
      } else if (error.response.status === 403) {
          throw new Error('权限不足，可能是跨域配置问题，请检查跨域相关设置。');
      } else if (error.response.status === 404) {
          throw new Error('请求的资源不存在，请检查路由是否正确。');
      } else if (error.response.status === 500) {
          throw new Error('后端服务器内部错误，请稍后再试。');
      }
  }
  throw new Error('未知错误，请检查网络连接及相关配置。');
}
};

export const runMolecularDynamics = async (file, mdParams) => {
  try {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('mdParams', JSON.stringify(mdParams));
    console.log('FormData详情,所有键值对:', formData.getAll('file'));
    console.log('FormData详情,查看整体结构:', [...formData.entries()]);
    const response = await axios.post(`${baseURL}/molecular-dynamics`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
    return response.data;
  } catch (error) {
    console.error('Error running molecular dynamics:', error);
    if (error.response) {
      if (error.response.status === 400) {
          throw new Error('请求格式错误，请检查文件及请求参数是否符合要求。');
      } else if (error.response.status === 403) {
          throw new Error('权限不足，可能是跨域配置问题，请检查跨域相关设置。');
      } else if (error.response.status === 404) {
          throw new Error('请求的资源不存在，请检查路由是否正确。');
      } else if (error.response.status === 500) {
          throw new Error('请稍后,如果长时间未响应，请联系管理员。');
      }
  }
  throw new Error('未知错误，请检查网络连接及相关配置。');
}
};

export const runStructureOptimization = async (file) => {
  try {
    console.log(file);
    const formData = new FormData();
    formData.append('file', file);
    console.log('FormData详情,所有键值对:', formData.getAll('file'));
    console.log('FormData详情,查看整体结构:', [...formData.entries()]);
    const response = await axios.post(`${baseURL}/structure-optimization`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
    return response.data;
  } catch (error) {
    console.error('Error running structure optimization:', error);
    if (error.response) {
      if (error.response.status === 400) {
          throw new Error('请求格式错误，请检查文件及请求参数是否符合要求。');
      } else if (error.response.status === 300) {
          throw new Error('权限不足，可能是跨域配置问题，请检查跨域相关设置。');
      } else if (error.response.status === 404) {
          throw new Error('请求的资源不存在，请检查路由是否正确。');
      } else if (error.response.status === 500) {
          throw new Error('后端服务器内部错误，请稍后再试。');
      }
  }
  throw new Error('未知错误，请检查网络连接及相关配置。');
}
};
