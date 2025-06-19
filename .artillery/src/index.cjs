const axios = require('axios');
const fs = require('fs');
const { spawn } = require('child_process');

const baseURL = process.env.API_BASE_URL


async function loginAsRoot() {
  try {
    const response = await axios.post(`${baseURL}/auth/login`, {
      email: process.env.SUPERUSER_EMAIL,
      password: process.env.SUPERUSER_PASSWORD
    });
    return response.data.access_token;
  } catch (error) {
    console.error('Erro ao fazer login como root:', error.message);
    process.exit(1);
  }
}

async function loginAsManager() {
  try {
    const response = await axios.post(`${baseURL}/auth/login`, {
      email: process.env.FAN_MANAGER_EMAIL,
      password: process.env.FAN_MANAGER_PASSWORD
    });
    return response.data.access_token;
  } catch (error) {
    console.error('Erro ao fazer login como manager:', error.message);
    process.exit(1);
  }
}

async function getFans(token) {
  try {
    const response = await axios.get(`${baseURL}/fans?page_size=10`, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });
    return response.data.data;
  } catch (error) {
    console.error('Erro ao obter a lista de fãs:', error.message);
    process.exit(1);
  }
}


async function getSchedules(token) {
  try {
    const response = await axios.get(`${baseURL}/schedules?page_size=10&ativo=true&consolidada=true`, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });
    return response.data.data;
  } catch (error) {
    console.error('Erro ao obter a lista de programações:', error.message);
    process.exit(1);
  }
}
async function getVideos(fans, token) {

  const targetDate = '2024-09-26';
  
  const videos = await Promise.all(fans.map(async ({ serial }) => {
    try {
      const response = await axios.get(`${baseURL}/fans/external/${serial}/schedule/videos?data=${targetDate}`, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });
      const videos = response.data.videos.map(({contrato_tipo, contrato_id, video}) => ({
        contrato_id,
        contrato_tipo,
        video_id: video.id,
        quantidade: Math.floor(Math.random() * 5000) + 1
      })) 
      return {
        serial,
        data: targetDate,
        videos
      }
    } catch (error) {
      console.error('Erro ao obter a lista de fãs:', error.message);
      process.exit(1);
    }
  }));
  return videos;
}

async function generateResultFile(managerToken, fans, schedules, videos) {
  const fanSerials = fans.map(fan => fan.serial);
  const schedulesDates = schedules.map(schedule => schedule.data);
  let csvScheduleContent = '';
  let csvFanContent = '';
  let csvVideoContent = '';
  schedulesDates.forEach(schedule => {
    fanSerials.forEach(serial => {
      csvScheduleContent += `${managerToken},${serial},${schedule}\n`;
    });
  });
  fanSerials.forEach(serial => {
    csvFanContent += `${managerToken},${serial}\n`;
  });
  videos.forEach(({serial, data, videos}) => {
    csvVideoContent += `${managerToken},${serial},${data},${btoa(JSON.stringify(videos))}'\n`;
  });
  fs.writeFileSync('schedule-data.csv', csvScheduleContent);
  fs.writeFileSync('fans-data.csv', csvFanContent);
  fs.writeFileSync('videos-data.csv', csvVideoContent);
}

async function runArtillery() {
  return new Promise((resolve, reject) => {
    const artilleryProcess = spawn('artillery', ['run', 'tests/load-test-config.yml', '--target', baseURL]);

    artilleryProcess.stdout.on('data', (data) => {
      console.log(`${data}`);
    });

    artilleryProcess.stderr.on('data', (data) => {
      console.error(`${data}`);
    });

    artilleryProcess.on('close', (code) => {
      if (code === 0) {
        resolve();
      } else {
        reject(new Error(`Artillery process exited with code ${code}`));
      }
    });
  });
}

async function main() {
  try {
    const rootToken = await loginAsRoot();

    const fans = await getFans(rootToken);

    const schedules = await getSchedules(rootToken);

    const videos = await getVideos(fans, rootToken);

    const managerToken = await loginAsManager();

    await generateResultFile(managerToken, fans, schedules, videos);

    await runArtillery();

    console.log('Teste de carga concluído com sucesso.');
  } catch (error) {
    console.error('Erro no processo:', error.message);
  } finally {
    if (fs.existsSync('tests-data.csv')) {
      fs.unlinkSync('tests-data.csv');
    }
  }
}

main();
