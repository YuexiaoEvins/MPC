<template>
  <div class="comment-wrap">
    <textarea class="comment-input" placeholder="请输入内容" id="textpanel" v-model="content"></textarea>
    <div class="opration">
      <div class="emoji-panel-btn" @click="showEmojiPanel">
        <img src="../../assets/img/face_logo.png" />
      </div>
      <div @click="saveComment" class="comment-send-btn comment-send-btn-bounce">发表评论</div>
      <emoji-panel @emojiClick="appendEmoji" v-if="isShowEmojiPanel"></emoji-panel>
    </div>
  </div>
</template>
<script>
import EmojiPanel from "./children/EmojiPanel.vue";
import api from '../../api/article';
import {getLocalStorage} from "../../utils/auth";
export default {
  data() {
    return {
      content: "",
      flag: false,
      isShowEmojiPanel: false,
      comments: [],
    };
  },
  components: {
    EmojiPanel
  },
  methods: {
    saveComment() {
      this.content = this.content.replace(/:.*?:/g, this.emoji)
      if(this.content.trim() !== ''){
        api.addMessageBoard({
          user_id: getLocalStorage('user_id'),
          content: this.content,
          token: getLocalStorage('token')
        }).then(res => {
          console.log(res);
          this.content = ''
          this.$message.success('留言成功')
          this.$emit('callBack',res.board)
          this.$emit('callBack1',res.board_count)
        })
        this.isShowEmojiPanel = false;
      }else {
        this.$message.warning('留言不可以为空')
      }
    },
    showEmojiPanel() {
      this.isShowEmojiPanel = !this.isShowEmojiPanel;
    },
    emoji(word) {
      // 生成html
      const type = word.substring(1, word.length - 1);
      return `<i class="emoji-item-common emoji-${type} emoji-size-small"></i>`;
    },
    appendEmoji(text) {
      const el = document.getElementById("textpanel");
      this.content = el.value + ":" + text + ":";
    }
  }
};
</script>
<style  lang="scss">
.comment-wrap {
  width: 680px;
  margin-bottom: 30px;
  .emoji-item-common {
    background: url("../../assets/img/emoji_sprite.png");
    display: inline-block;
    &:hover {
      cursor: pointer;
    }
  }
  .emoji-size-small {
    // 表情大小
    zoom: 0.3;
  }
  .emoji-size-large {
    zoom: 0.5; // emojipanel表情大小
    margin: 4px;
  }
  .comments-list {
    margin-top: 20px;
    .comments-list-item {
      margin-bottom: 20px;
      .comments-list-item-heading {
        display: inline-block;
        img {
          height: 32px;
          width: 32px;
          border-radius: 50%;
          vertical-align: middle;
        }
        .comments-list-item-username {
          margin-left: 5px;
          font-weight: bold;
        }
      }
      .comments-list-item-content {
        margin: 10px 0px;
        border-bottom: 1px solid #cccccc;
        &:last-child {
          border-bottom: 0;
        }
        span {
          vertical-align: top;
        }
      }
    }
  }
  .comment-input {
    height: 100px;
    width: 680px;
    border: 1px solid #cccccc;
    border-radius: 5px;
    padding: 10px;
    resize: none;
    &:focus {
      outline: none;
    }
  }
  .opration {
    width: 522px;
    display: flex;
    justify-content: space-between;
    position: relative;
    .emoji-panel-btn {
      &:hover {
        cursor: pointer;
        opacity: 0.8;
      }
      img {
        height: 24px;
        width: 24px;
      }
    }
    .comment-send-btn {
      width: 80px;
      height: 30px;
      line-height: 30px;
      text-align: center;
      right: -175px;
      margin-top: 2px;
      border: 1px solid #1da1f2;
      border-radius: 100px;
      box-sizing: border-box;
      font-weight: bold;
      font-size: 13px;
      color: #ffffff;
      background-color: #4ab3f4;
      &:hover {
        cursor: pointer;
      }
    }
    .comment-send-btn-bounce {
      position: relative;
    }
    .comment-send-btn-bounce:focus {
      outline: none;
    }
    .comment-send-btn-bounce:after {
      content: "";
      display: block;
      position: absolute;
      top: 0px;
      left: 0px;
      right: 0px;
      bottom: 0px;
      border-radius: 100px;
      border: 0px solid #1da1f2;
      opacity: 0.7;
      transition: all 0.1s;
    }
    .comment-send-btn-bounce:active:after {
      //.bounce active时 伪元素:after的样式
      opacity: 1;
      top: -5px;
      left: -5px;
      right: -5px;
      bottom: -5px;
      border-radius: 100px;
      border: 2px solid #1da1f2;
      transition: all 0.2s;
    }
  }
}
@import "../../assets/css/emoji.css"; // 导入精灵图样式
</style>
