
#include <stdio.h>
#include "AquesTalk.h"

#using "AquesTalk.dll"


int main(int ac, char **av)
{
 // 声質パラメータ
 AQTK_VOICE voice = gVoice_F1;
 voice.spd = 120;
 int size;
 unsigned char *wav = AquesTalk_Synthe(&voice, "こんにちわ。", &size);
 if(wav==0) {
 fprintf(stderr, "ERR %d", size); // エラー時は size にエラーコードが返る
 return -1;
 }
 // ルートディレクトリに生成した音声データを保存
 FILE *fp = fopen("\\ZZZ.wav", "wb");
 fwrite(wav, 1, size, fp);
 fclose(fp);
 // Synthe()で生成した音声データは、使用後に呼び出し側で解放する
 AquesTalk_FreeWave (wav);
 return 0;
}